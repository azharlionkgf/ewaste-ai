"""
E-Waste AI — Video Analysis Page
==================================
Analyse short e-waste video clips frame-by-frame using available
image-classification models. If no model is loaded the page clearly
communicates that the feature is unavailable.
"""

import os, sys, tempfile, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from frontend.theme import apply_theme, page_header, section_header, status_badge, COLORS

# ── optional imports ───────────────────────────────────────────────────
try:
    import cv2
    CV2_OK = True
except ImportError:
    CV2_OK = False

try:
    from backend.services.ai_model_service import AIModelService
    AI_OK = True
except Exception:
    AI_OK = False


def render_video_analysis():
    apply_theme()
    page_header(
        "Video Analysis",
        "Frame-by-frame e-waste classification from video clips",
        "🎥",
    )

    # ── capability check ───────────────────────────────────────────────
    if not CV2_OK:
        st.warning("⚠️ OpenCV is not installed. Video processing is unavailable in this environment.")
        st.info("Install `opencv-python-headless` and restart the application to enable video analysis.")
        return

    if not AI_OK:
        st.warning("⚠️ AI Model Service could not be loaded. Video inference is unavailable.")
        return

    # ── model availability ─────────────────────────────────────────────
    try:
        svc = AIModelService()
        available = svc.list_available_models()
    except Exception as e:
        st.error(f"Could not connect to AI Model Service: {e}")
        return

    image_models = [m for m in available if "image" in m.get("task_type", "").lower()
                    or "classif" in m.get("task_type", "").lower()]

    if not image_models:
        st.warning("🤖 No image/video classification model is currently deployed.")
        st.info("Train and register an image classification model in the **Model Training** workspace first.")
        return

    # ── upload ─────────────────────────────────────────────────────────
    section_header("Upload Video Clip", "Supported: MP4, AVI, MOV — max 100 MB")

    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded = st.file_uploader(
            "Drop your e-waste video here",
            type=["mp4", "avi", "mov"],
            help="Max 100 MB. The clip is analysed frame-by-frame.",
        )
    with col2:
        model_names = [f"{m['name']} v{m.get('version','?')}" for m in image_models]
        selected_idx = st.selectbox("Classification Model", range(len(model_names)),
                                    format_func=lambda i: model_names[i])
        frame_step = st.slider("Sample every N frames", 1, 30, 10,
                               help="Higher = faster but less accurate")
        conf_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.05)

    if not uploaded:
        st.markdown(
            f"""<div style='background:#1C1C1C;border:2px dashed #2D2D2D;border-radius:12px;
            padding:3rem;text-align:center;color:#666'>
            <div style='font-size:3rem'>🎥</div>
            <div style='font-size:1.1rem;margin-top:1rem'>Upload a video clip to begin analysis</div>
            <div style='font-size:0.8rem;margin-top:0.5rem'>MP4 · AVI · MOV — max 100 MB</div>
            </div>""",
            unsafe_allow_html=True,
        )
        return

    # ── size guard ─────────────────────────────────────────────────────
    size_mb = len(uploaded.getvalue()) / 1024 / 1024
    if size_mb > 100:
        st.error(f"File is {size_mb:.1f} MB — maximum allowed is 100 MB.")
        return

    st.success(f"✅ Uploaded: **{uploaded.name}** — {size_mb:.2f} MB")

    if st.button("🔍 Analyse Video", type="primary"):
        selected_model = image_models[selected_idx]

        with tempfile.NamedTemporaryFile(suffix=os.path.splitext(uploaded.name)[1], delete=False) as tmp:
            tmp.write(uploaded.getvalue())
            tmp_path = tmp.name

        try:
            cap = cv2.VideoCapture(tmp_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
            duration = total_frames / fps

            st.markdown(f"**Video info:** {total_frames} frames · {fps:.1f} FPS · {duration:.1f}s")

            frame_indices = list(range(0, total_frames, frame_step))
            if not frame_indices:
                st.error("No frames found in video.")
                cap.release()
                return

            st.markdown(f"Sampling **{len(frame_indices)}** frames …")
            progress = st.progress(0)
            status_text = st.empty()

            results = []
            for i, fi in enumerate(frame_indices):
                cap.set(cv2.CAP_PROP_POS_FRAMES, fi)
                ok, frame = cap.read()
                if not ok:
                    continue

                # Convert BGR→RGB, then to PIL bytes
                from PIL import Image
                import io
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(rgb)
                buf = io.BytesIO()
                pil_img.save(buf, format="JPEG", quality=85)
                img_bytes = buf.getvalue()

                try:
                    pred = svc.predict(
                        model_id=selected_model["model_id"],
                        input_data={"image_bytes": img_bytes},
                    )
                    conf = pred.get("confidence", 0.0)
                    label = pred.get("predicted_class", "unknown")
                    if conf >= conf_threshold:
                        results.append({
                            "frame": fi,
                            "time_s": round(fi / fps, 2),
                            "label": label,
                            "confidence": round(conf, 4),
                        })
                except Exception as ex:
                    results.append({
                        "frame": fi,
                        "time_s": round(fi / fps, 2),
                        "label": f"error: {ex}",
                        "confidence": 0.0,
                    })

                progress.progress((i + 1) / len(frame_indices))
                status_text.text(f"Frame {fi}/{total_frames}")

            cap.release()
            progress.progress(1.0)
            status_text.text("✅ Analysis complete")

        finally:
            try:
                os.remove(tmp_path)
            except Exception:
                pass

        # ── results ───────────────────────────────────────────────────
        if not results:
            st.warning("No frames passed the confidence threshold. Lower the threshold and retry.")
            return

        section_header("Analysis Results")

        import pandas as pd
        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True)

        # Summary
        from collections import Counter
        counts = Counter(r["label"] for r in results)
        top_label, top_count = counts.most_common(1)[0]
        avg_conf = sum(r["confidence"] for r in results) / len(results)

        c1, c2, c3 = st.columns(3)
        c1.metric("Frames Analysed", len(results))
        c2.metric("Dominant Class", top_label)
        c3.metric("Avg Confidence", f"{avg_conf:.2%}")

        st.warning(
            "⚠️ **Disclaimer:** These are AI model predictions, not certified classifications. "
            "Results may vary with video quality and lighting conditions."
        )

        # Download
        csv = df.to_csv(index=False).encode()
        st.download_button("⬇️ Download Results (CSV)", csv,
                           file_name="video_analysis_results.csv", mime="text/csv")
