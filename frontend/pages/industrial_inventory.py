"""
E-Waste AI — Industrial Operations & Inventory Workspace
==========================================================
Task 8 of Phase 5 / Phase 6 integration.
Uses actual DB column names from all_models.py inspection.
"""

import os, sys, uuid as _uuid_mod
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from datetime import datetime, date
from frontend.theme import apply_theme, page_header, section_header, status_badge, COLORS

try:
    from backend.database import SessionLocal
    from backend.models.all_models import (
        WasteBatch, Device, RecoveryRecord, Inventory,
    )
    DB_OK = True
except Exception as e:
    DB_OK = False
    DB_ERR = str(e)


def _db():
    return SessionLocal() if DB_OK else None


def _status_color(status: str) -> str:
    return {"incoming": "info", "sorting": "warning", "dismantling": "warning",
            "processing": "gold", "completed": "success", "rejected": "error"}.get(
        (status or "").lower(), "info")


def render_industrial_inventory():
    apply_theme()
    page_header("Industrial Operations",
                "E-waste batch registration, device tracking, dismantling and inventory management", "🏭")

    if not DB_OK:
        st.error(f"Database unavailable: {DB_ERR}"); return

    tabs = st.tabs(["📦 Batches", "🖥️ Devices", "⚗️ Material Recovery", "🗄️ Inventory"])

    # ── TAB 1: BATCHES ─────────────────────────────────────────────────
    with tabs[0]:
        section_header("Incoming E-Waste Batches")
        with st.expander("➕ Register New Batch", expanded=False):
            with st.form("new_batch"):
                c1, c2 = st.columns(2)
                batch_number = c1.text_input("Batch Number (auto if blank)")
                source = c2.text_input("Source / Supplier", placeholder="e.g. City Municipality")
                waste_type = c1.selectbox("Waste Category", [
                    "mixed_ewaste","computers","mobile_phones","televisions",
                    "printers","batteries","cables","other"])
                weight_kg = c2.number_input("Total Weight (kg)", min_value=0.0, step=0.5)
                received_date = c1.date_input("Received Date", value=date.today())
                location = c2.text_input("Storage Location")
                notes = st.text_area("Notes")
                sub = st.form_submit_button("Register Batch", type="primary")
            if sub:
                db = _db()
                try:
                    b = WasteBatch(
                        batch_number=batch_number.strip() or f"BATCH-{_uuid_mod.uuid4().hex[:8].upper()}",
                        source=source or "Unknown",
                        waste_category=waste_type,
                        total_weight_kg=weight_kg,
                        received_date=received_date.isoformat(),
                        status="incoming",
                        location=location,
                        notes=notes,
                        created_at=datetime.utcnow(),
                    )
                    db.add(b); db.commit()
                    st.success(f"✅ Batch **{b.batch_number}** registered.")
                except Exception as ex:
                    db.rollback(); st.error(f"Failed: {ex}")
                finally:
                    db.close()

        db = _db()
        try:
            batches = db.query(WasteBatch).order_by(WasteBatch.created_at.desc()).all()
        except Exception as ex:
            st.error(f"Load error: {ex}"); batches = []
        finally:
            db.close()

        if not batches:
            st.info("No batches registered yet.")
        else:
            for b in batches:
                sb = status_badge(b.status or "unknown", _status_color(b.status or ""))
                status_icon = {"completed": "🟢", "rejected": "🔴", "processing": "🟡", "sorting": "🟠", "dismantling": "🟠"}.get((b.status or "").lower(), "🔵")
                with st.expander(f"📦 {b.batch_number} — {b.waste_category} — {b.total_weight_kg} kg · {status_icon} {b.status or 'unknown'}"):
                    st.markdown(sb, unsafe_allow_html=True)
                    c1, c2, c3 = st.columns(3)
                    c1.markdown(f"**Source:** {b.source}")
                    c1.markdown(f"**Category:** {b.waste_category}")
                    c2.markdown(f"**Weight:** {b.total_weight_kg} kg")
                    c2.markdown(f"**Received:** {b.received_date}")
                    c3.markdown(f"**Location:** {b.location or '—'}")
                    c3.markdown(f"**Status:** {b.status}")
                    if b.notes:
                        st.caption(b.notes)
                    new_st = st.selectbox("Update Status",
                        ["incoming","sorting","dismantling","processing","completed","rejected"],
                        index=["incoming","sorting","dismantling","processing","completed","rejected"].index(b.status or "incoming"),
                        key=f"st_{b.id}")
                    if st.button("Save", key=f"sv_{b.id}"):
                        db2 = _db()
                        try:
                            r = db2.query(WasteBatch).filter(WasteBatch.id == b.id).first()
                            if r:
                                r.status = new_st; r.updated_at = datetime.utcnow()
                                db2.commit(); st.success("Updated."); st.rerun()
                        except Exception as ex:
                            db2.rollback(); st.error(str(ex))
                        finally:
                            db2.close()

    # ── TAB 2: DEVICES ─────────────────────────────────────────────────
    with tabs[1]:
        section_header("Device Registry")
        db = _db()
        try:
            batch_opts = db.query(WasteBatch).all()
        except Exception:
            batch_opts = []
        finally:
            db.close()

        if not batch_opts:
            st.info("Register at least one batch before adding devices.")
        else:
            with st.expander("➕ Add Device"):
                with st.form("new_device"):
                    bmap = {b.batch_number: b.id for b in batch_opts}
                    sel = st.selectbox("Batch", list(bmap.keys()))
                    c1, c2 = st.columns(2)
                    dtype = c1.selectbox("Device Type", ["laptop","desktop","mobile_phone","tablet",
                        "television","monitor","printer","keyboard","battery_pack","router","hard_drive","other"])
                    brand = c2.text_input("Manufacturer / Brand")
                    model_name = c1.text_input("Model Name")
                    condition = c2.selectbox("Condition", ["unknown","poor","fair","good","excellent"])
                    weight_kg = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
                    sub_d = st.form_submit_button("Add Device", type="primary")
                if sub_d:
                    db3 = _db()
                    try:
                        dev = Device(batch_id=bmap[sel], device_type=dtype,
                                     manufacturer=brand or "Unknown", model_name=model_name or "",
                                     condition=condition, weight_kg=weight_kg,
                                     created_at=datetime.utcnow())
                        db3.add(dev); db3.commit()
                        st.success(f"✅ {dtype} added to {sel}.")
                    except Exception as ex:
                        db3.rollback(); st.error(str(ex))
                    finally:
                        db3.close()

            import pandas as pd
            db4 = _db()
            try:
                devs = db4.query(Device).order_by(Device.created_at.desc()).limit(100).all()
            except Exception as ex:
                st.error(str(ex)); devs = []
            finally:
                db4.close()
            if devs:
                st.dataframe(pd.DataFrame([{
                    "Type": d.device_type, "Manufacturer": d.manufacturer,
                    "Model": d.model_name, "Condition": d.condition,
                    "Weight kg": d.weight_kg, "AI Category": d.ai_predicted_category or "—",
                    "AI Conf": f"{d.ai_confidence:.2f}" if d.ai_confidence else "—",
                } for d in devs]), use_container_width=True)

    # ── TAB 3: RECOVERY ─────────────────────────────────────────────────
    with tabs[2]:
        section_header("Recovery Records")
        db5 = _db()
        try:
            proc_batches = db5.query(WasteBatch).filter(
                WasteBatch.status.in_(["processing","completed"])).all()
        except Exception:
            proc_batches = []
        finally:
            db5.close()

        if not proc_batches:
            st.info("No batches in 'processing' or 'completed' status.")
        else:
            with st.expander("➕ Log Recovery Record"):
                with st.form("rec_form"):
                    bmap2 = {b.batch_number: b.id for b in proc_batches}
                    sel2 = st.selectbox("Batch", list(bmap2.keys()))
                    c1, c2 = st.columns(2)
                    mat = c1.selectbox("Material", ["gold","silver","copper","aluminum","steel","iron",
                        "palladium","platinum","lithium","cobalt","plastic","glass","circuit_boards","other"])
                    qty_g = c2.number_input("Quantity Recovered (grams)", min_value=0.0, step=0.1)
                    method = c1.selectbox("Recovery Method", ["manual_dismantling","shredding",
                        "hydrometallurgy","pyrometallurgy","electrochemical","other"])
                    rec_rate = c2.number_input("Recovery Rate %", 0.0, 100.0, step=0.1)
                    notes_r = st.text_area("Notes")
                    sub_r = st.form_submit_button("Log Recovery", type="primary")
                if sub_r:
                    db6 = _db()
                    try:
                        rr = RecoveryRecord(batch_id=bmap2[sel2], material_name=mat,
                                            recovered_quantity_g=qty_g, recovery_method=method,
                                            recovery_rate_percent=rec_rate, notes=notes_r,
                                            value_source="measured", recorded_at=datetime.utcnow())
                        db6.add(rr); db6.commit()
                        st.success(f"✅ Logged {qty_g} g of {mat}.")
                    except Exception as ex:
                        db6.rollback(); st.error(str(ex))
                    finally:
                        db6.close()

        import pandas as pd
        db7 = _db()
        try:
            recs = db7.query(RecoveryRecord).order_by(RecoveryRecord.recorded_at.desc()).limit(100).all()
        except Exception as ex:
            st.error(str(ex)); recs = []
        finally:
            db7.close()
        if recs:
            st.dataframe(pd.DataFrame([{
                "Batch": r.batch_id, "Material": r.material_name,
                "Qty (g)": r.recovered_quantity_g, "Rate %": r.recovery_rate_percent,
                "Method": r.recovery_method, "Est Value $": r.estimated_value_usd or "—",
                "Date": str(r.recorded_at)[:10] if r.recorded_at else "—",
            } for r in recs]), use_container_width=True)
            total_g = sum(r.recovered_quantity_g or 0 for r in recs)
            st.metric("Total Recovered", f"{total_g:.1f} g ({total_g/1000:.3f} kg)")
        else:
            st.info("No recovery records yet.")

    # ── TAB 4: INVENTORY ───────────────────────────────────────────────
    with tabs[3]:
        section_header("Material Inventory")
        with st.expander("➕ Update Inventory"):
            with st.form("inv_form"):
                c1, c2 = st.columns(2)
                inv_mat = c1.selectbox("Material", ["gold","silver","copper","aluminum","steel",
                    "palladium","platinum","lithium","cobalt","plastic","glass","circuit_boards","other"],
                    key="inv_m")
                inv_qty_g = c2.number_input("Quantity (grams)", min_value=0.0, step=0.1, key="inv_q")
                inv_loc = c1.text_input("Location", key="inv_l")
                inv_src = c2.selectbox("Source", ["measured","estimated","ai_predicted","user_provided"],
                                       key="inv_s")
                sub_inv = st.form_submit_button("Update", type="primary")
            if sub_inv:
                db8 = _db()
                try:
                    ex_item = db8.query(Inventory).filter(Inventory.material_name == inv_mat).first()
                    if ex_item:
                        ex_item.quantity_g = (ex_item.quantity_g or 0) + inv_qty_g
                        ex_item.location = inv_loc or ex_item.location
                        ex_item.updated_at = datetime.utcnow()
                    else:
                        db8.add(Inventory(material_name=inv_mat, quantity_g=inv_qty_g,
                                          location=inv_loc, source=inv_src,
                                          updated_at=datetime.utcnow()))
                    db8.commit()
                    st.success(f"✅ Inventory updated: {inv_mat} +{inv_qty_g} g")
                except Exception as ex:
                    db8.rollback(); st.error(str(ex))
                finally:
                    db8.close()

        import pandas as pd
        db9 = _db()
        try:
            inv_items = db9.query(Inventory).order_by(Inventory.material_name).all()
        except Exception as ex:
            st.error(str(ex)); inv_items = []
        finally:
            db9.close()
        if inv_items:
            st.dataframe(pd.DataFrame([{
                "Material": i.material_name, "Qty (g)": i.quantity_g,
                "Qty (kg)": round((i.quantity_g or 0)/1000, 4),
                "Location": i.location or "—", "Source": i.source or "—",
                "Updated": str(i.updated_at)[:10] if i.updated_at else "—",
            } for i in inv_items]), use_container_width=True)
            total_g = sum(i.quantity_g or 0 for i in inv_items)
            st.metric("Total Inventory", f"{total_g:.1f} g ({total_g/1000:.3f} kg)")
        else:
            st.info("Inventory empty.")
