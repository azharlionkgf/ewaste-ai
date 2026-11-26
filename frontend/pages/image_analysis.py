"""
frontend/pages/image_analysis.py
E-WASTE AI - Image & Video Analysis Page
Upload e-waste images/video frames, run AI classification, view results.
"""

import streamlit as st
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from frontend.theme import apply_theme, section_header


def render():
    apply_theme()
    st.markdown('<h1 class="page-title">🖼️ Image & Video Analysis</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Upload e-waste images or video files and classify them using trained AI models.</p>',
        unsafe_allow_html=True
    )

    tabs = st.tabs(["📷 Image Classification", "🎞️ Video Frame Analysis", "📊 Batch Analysis"])

    with tabs[0]:
        _tab_image()
    with tabs[1]:
        _tab_video()
    with tabs[2]:
        _tab_batch()


# ============================================================
# TAB 1 — IMAGE CLASSIFICATION
# ============================================================
def _tab_image():
    section_header("Image Classification", "Upload an e-waste image and classify it.")

    # Model selection
    active_model_path = st.session_state.get("active_model_path")
    active_model_meta = st.session_state.get("active_model_meta", {})

    if not active_model_path:
        st.warning("""
        **No active model selected.**
        
        Go to **Model Training** → **Saved Models** tab and click **Use for Prediction** on a trained model.
        
        If you haven't trained a model yet, go to **Dataset Management** to upload and prepare your dataset.
        """)

        # Still allow showing the UI for demonstration
        demo_mode = st.checkbox("Show demo mode (rule-based estimates only)", value=False, key="demo_mode_img")
        if not demo_mode:
            return

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### Upload Image")
        uploaded = st.file_uploader(
            "Upload e-waste image",
            type=["jpg", "jpeg", "png", "bmp", "webp"],
            key="img_analysis_upload"
        )

        top_k = st.slider("Top K Predictions", 1, 10, 5, key="img_top_k")

        if uploaded and st.button("🔍 Classify Image", type="primary", key="btn_classify_img"):
            _classify_image(uploaded, top_k, active_model_path, active_model_meta)

    with col2:
        if uploaded:
            st.markdown("#### Uploaded Image")
            st.image(uploaded, use_container_width=True)

    # Results
    if "img_classification_result" in st.session_state:
        _show_image_result(st.session_state["img_classification_result"])


def _classify_image(uploaded_file, top_k: int, model_path: str, model_meta: dict):
    import tempfile, os
    try:
        tmp_dir = Path(tempfile.mkdtemp())
        tmp_path = tmp_dir / uploaded_file.name
        with open(tmp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("Running AI classification..."):
            if model_path:
                from ml.inference.predictor import ModelPredictor
                model_type = model_meta.get("model_type", "cnn")
                class_names = model_meta.get("class_names", [])
                predictor = ModelPredictor(model_path, model_type, class_names, device="cpu")
                predictor.load_model()
                results = predictor.predict_image(str(tmp_path), top_k=top_k)
            else:
                # Demo mode: rule-based fallback
                results = _demo_classify_image(uploaded_file.name)

        st.session_state["img_classification_result"] = {
            "predictions": results,
            "image_name": uploaded_file.name,
            "model_used": model_meta.get("model_name", "demo") if model_path else "rule_based_demo",
        }

    except Exception as e:
        st.error(f"Classification failed: {e}")
        import traceback
        st.code(traceback.format_exc())


def _demo_classify_image(filename: str) -> list:
    """Fallback demo classifications (clearly labeled as demo/estimates)."""
    import random
    categories = ["smartphone", "laptop", "circuit_board", "battery", "monitor_lcd", "charger", "cable"]
    top = random.choice(categories)
    remaining = [c for c in categories if c != top]
    random.shuffle(remaining)
    base_conf = round(random.uniform(0.40, 0.75), 4)
    results = [{"rank": 1, "class_name": top, "confidence": base_conf, "is_estimate": True}]
    leftover = round(1 - base_conf, 4)
    for i, cat in enumerate(remaining[:4], start=2):
        conf = round(leftover / (5 - i + 2), 4)
        results.append({"rank": i, "class_name": cat, "confidence": conf, "is_estimate": True})
    return results


def _show_image_result(result: dict):
    st.markdown("---")
    st.markdown("### 🎯 Classification Results")
    st.caption(f"Model: **{result['model_used']}** | Image: **{result['image_name']}**")

    preds = result["predictions"]
    if not preds:
        st.warning("No predictions returned.")
        return

    if preds[0].get("error"):
        st.error(f"Prediction error: {preds[0].get('error')}")
        return

    top = preds[0]
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Top Prediction", top.get("class_name", "—").replace("_", " ").title())
    with col2:
        conf_pct = round(top.get("confidence", 0) * 100, 1)
        st.metric("Confidence", f"{conf_pct}%")
    with col3:
        is_est = top.get("is_estimate", False)
        st.metric("Status", "🔮 Estimate" if is_est else "✅ AI Prediction")

    if top.get("is_estimate"):
        st.warning("⚠️ **Demo mode** — these are random estimates, not real AI predictions. Train a model first.")

    # Confidence bar chart
    st.markdown("#### All Predictions")
    import pandas as pd
    pred_df = pd.DataFrame([
        {
            "Rank": p.get("rank"),
            "Category": p.get("class_name", "").replace("_", " ").title(),
            "Confidence": p.get("confidence", 0),
            "Confidence %": f"{p.get('confidence', 0)*100:.1f}%",
        }
        for p in preds
    ])
    st.dataframe(pred_df, use_container_width=True, hide_index=True)
    st.bar_chart(pred_df.set_index("Category")["Confidence"])

    # Recovery hints for top prediction
    _show_recovery_hints(top.get("class_name", ""))


def _show_recovery_hints(device_type: str):
    if not device_type:
        return
    try:
        from industrial.operations.classification_workflow import DEVICE_MATERIAL_ESTIMATES
        mat = DEVICE_MATERIAL_ESTIMATES.get(device_type, DEVICE_MATERIAL_ESTIMATES.get("default"))
        if mat:
            st.markdown("---")
            st.markdown(f"#### 🔩 Estimated Material Composition — *{device_type.replace('_', ' ').title()}*")
            st.caption(f"Source: {mat.get('source', 'Research averages')} — All values are estimates (is_estimate=True)")
            import pandas as pd
            mat_items = {k: v for k, v in mat.items() if k not in ("is_estimate", "source", "unit") and isinstance(v, (int, float))}
            if mat_items:
                mat_df = pd.DataFrame([
                    {"Material": k.replace("_pct", "").replace("_", " ").title(), "Estimate": f"{v}%"}
                    for k, v in mat_items.items()
                ])
                st.dataframe(mat_df, use_container_width=True, hide_index=True)
    except Exception:
        pass


# ============================================================
# TAB 2 — VIDEO FRAME ANALYSIS
# ============================================================
def _tab_video():
    section_header("Video Frame Analysis", "Extract frames from e-waste video and classify each frame.")

    active_model_path = st.session_state.get("active_model_path")

    uploaded_video = st.file_uploader(
        "Upload e-waste video",
        type=["mp4", "avi", "mov", "mkv"],
        key="video_analysis_upload"
    )

    if not uploaded_video:
        st.info("""
        Upload a video of e-waste items. The system will:
        1. Extract frames at regular intervals
        2. Classify each frame using the active AI model
        3. Aggregate results across all frames
        """)
        return

    col1, col2 = st.columns(2)
    with col1:
        frame_interval = st.slider("Extract every N seconds", 1, 10, 2, key="video_frame_interval")
        max_frames = st.number_input("Maximum frames to analyze", 5, 100, 20, key="video_max_frames")

    with col2:
        st.info(f"**Video:** {uploaded_video.name} ({uploaded_video.size / 1024:.1f} KB)")
        if not active_model_path:
            st.warning("No active model. Set one in Model Training → Saved Models.")

    if st.button("🎞️ Extract & Analyze Frames", type="primary", key="btn_analyze_video", disabled=not active_model_path):
        _analyze_video(uploaded_video, frame_interval, max_frames, active_model_path)

    if "video_analysis_result" in st.session_state:
        _show_video_result(st.session_state["video_analysis_result"])


def _analyze_video(uploaded_video, frame_interval: int, max_frames: int, model_path: str):
    try:
        import cv2
        import tempfile, numpy as np
        from ml.inference.predictor import ModelPredictor

        tmp_dir = Path(tempfile.mkdtemp())
        video_path = tmp_dir / uploaded_video.name
        with open(video_path, "wb") as f:
            f.write(uploaded_video.getbuffer())

        with st.spinner("Extracting and analyzing frames..."):
            cap = cv2.VideoCapture(str(video_path))
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_step = max(1, int(fps * frame_interval))

            meta = st.session_state.get("active_model_meta", {})
            class_names = meta.get("class_names", [])
            predictor = ModelPredictor(model_path, meta.get("model_type", "cnn"), class_names)
            predictor.load_model()

            frame_results = []
            frame_idx = 0
            analyzed = 0

            progress = st.progress(0)
            while cap.isOpened() and analyzed < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                if frame_idx % frame_step == 0:
                    frame_path = tmp_dir / f"frame_{frame_idx:06d}.jpg"
                    cv2.imwrite(str(frame_path), frame)
                    preds = predictor.predict_image(str(frame_path), top_k=3)
                    frame_results.append({"frame": frame_idx, "predictions": preds})
                    analyzed += 1
                    progress.progress(min(analyzed / max_frames, 1.0))
                frame_idx += 1
            cap.release()

        st.session_state["video_analysis_result"] = {
            "total_frames_analyzed": analyzed,
            "frame_results": frame_results,
            "video_name": uploaded_video.name,
        }
        st.success(f"✅ Analyzed {analyzed} frames!")

    except ImportError:
        st.error("OpenCV not installed. Install with: `pip install opencv-python-headless`")
    except Exception as e:
        st.error(f"Video analysis failed: {e}")
        import traceback
        st.code(traceback.format_exc())


def _show_video_result(result: dict):
    st.markdown("---")
    st.markdown(f"### 🎞️ Video Analysis — {result['video_name']}")
    st.metric("Frames Analyzed", result["total_frames_analyzed"])

    import pandas as pd
    rows = []
    for fr in result["frame_results"]:
        top = fr["predictions"][0] if fr["predictions"] else {}
        rows.append({
            "Frame": fr["frame"],
            "Top Prediction": top.get("class_name", "—"),
            "Confidence": f"{top.get('confidence', 0)*100:.1f}%",
        })
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        # Aggregate majority vote
        from collections import Counter
        all_preds = [fr["predictions"][0].get("class_name", "") for fr in result["frame_results"] if fr["predictions"]]
        majority = Counter(all_preds).most_common(1)
        if majority:
            st.success(f"🎯 **Most frequent classification: {majority[0][0].replace('_', ' ').title()}** ({majority[0][1]} frames)")


# ============================================================
# TAB 3 — BATCH ANALYSIS
# ============================================================
def _tab_batch():
    section_header("Batch Image Analysis", "Classify multiple images at once.")

    active_model_path = st.session_state.get("active_model_path")
    if not active_model_path:
        st.warning("No active model selected. Set one in Model Training → Saved Models.")
        return

    uploaded_files = st.file_uploader(
        "Upload multiple e-waste images",
        type=["jpg", "jpeg", "png", "bmp"],
        accept_multiple_files=True,
        key="batch_analysis_upload"
    )

    if not uploaded_files:
        st.info("Upload multiple images to classify them all at once.")
        return

    st.info(f"**{len(uploaded_files)} images** selected.")

    if st.button("🔍 Classify All Images", type="primary", key="btn_batch_classify"):
        _run_batch_classify(uploaded_files, active_model_path)

    if "batch_results" in st.session_state:
        _show_batch_results(st.session_state["batch_results"])


def _run_batch_classify(files, model_path: str):
    import tempfile
    try:
        from ml.inference.predictor import ModelPredictor
        meta = st.session_state.get("active_model_meta", {})
        predictor = ModelPredictor(model_path, meta.get("model_type", "cnn"), meta.get("class_names", []))
        predictor.load_model()

        tmp_dir = Path(tempfile.mkdtemp())
        progress = st.progress(0)
        results = []

        for i, f in enumerate(files):
            tmp_path = tmp_dir / f.name
            with open(tmp_path, "wb") as fp:
                fp.write(f.getbuffer())
            preds = predictor.predict_image(str(tmp_path), top_k=3)
            top = preds[0] if preds else {}
            results.append({
                "File": f.name,
                "Top Prediction": top.get("class_name", "—").replace("_", " ").title(),
                "Confidence": f"{top.get('confidence', 0)*100:.1f}%",
                "Action": top.get("recommended_action", "review"),
            })
            progress.progress((i + 1) / len(files))

        st.session_state["batch_results"] = results
        st.success(f"✅ Classified {len(results)} images!")

    except Exception as e:
        st.error(f"Batch classification failed: {e}")


def _show_batch_results(results: list):
    import pandas as pd
    st.markdown("---")
    st.markdown("### Batch Classification Results")
    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Download CSV
    csv = df.to_csv(index=False)
    st.download_button("⬇️ Download Results CSV", csv, "batch_results.csv", "text/csv", key="dl_batch_csv")
