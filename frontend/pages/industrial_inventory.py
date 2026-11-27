"""
E-Waste AI — Industrial Operations & Inventory Workspace
==========================================================
Task 8 of Phase 5.
Register incoming e-waste, manage batches, devices, sorting
records, dismantling records, components, materials and inventory.
Connects to backend.services.batch_service and DB models.
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from datetime import datetime, date
from frontend.theme import apply_theme, page_header, section_header, status_badge, COLORS

# ── backend imports ────────────────────────────────────────────────────
try:
    from backend.database import SessionLocal
    from backend.models.all_models import (
        WasteBatch, Device, Component, Material,
        RecoveryRecord, Inventory,
    )
    DB_OK = True
except Exception as e:
    DB_OK = False
    DB_ERR = str(e)

try:
    from backend.services.batch_service import BatchManagementService
    BATCH_SVC_OK = True
except Exception as e:
    BATCH_SVC_OK = False
    BATCH_SVC_ERR = str(e)


# ── helpers ────────────────────────────────────────────────────────────

def _db():
    if not DB_OK:
        return None
    return SessionLocal()


def _status_color(status: str) -> str:
    colors = {
        "incoming": "info", "sorting": "warning", "dismantling": "warning",
        "processing": "gold", "completed": "success", "rejected": "error",
    }
    return colors.get(status.lower(), "info")


def render_industrial_inventory():
    apply_theme()
    page_header(
        "Industrial Operations",
        "E-waste batch registration, device tracking, dismantling and inventory management",
        "🏭",
    )

    if not DB_OK:
        st.error(f"Database unavailable: {DB_ERR}")
        return

    tabs = st.tabs(["📦 Batches", "🖥️ Devices & Components", "⚗️ Material Recovery", "🗄️ Inventory"])

    # ── TAB 1: BATCHES ─────────────────────────────────────────────────
    with tabs[0]:
        section_header("Incoming E-Waste Batches", "Register and track batches through the processing pipeline")

        with st.expander("➕ Register New Batch", expanded=False):
            with st.form("new_batch_form"):
                c1, c2 = st.columns(2)
                batch_id = c1.text_input("Batch ID (auto if blank)")
                source = c2.text_input("Source / Supplier", placeholder="e.g. City Municipality")
                waste_type = c1.selectbox("Waste Category", [
                    "mixed_ewaste", "computers", "mobile_phones", "televisions",
                    "printers", "batteries", "cables", "other",
                ])
                weight_kg = c2.number_input("Total Weight (kg)", min_value=0.0, step=0.5)
                received_date = c1.date_input("Received Date", value=date.today())
                notes = st.text_area("Notes", placeholder="Optional notes about condition, origin, etc.")
                submitted = st.form_submit_button("Register Batch", type="primary")

            if submitted:
                db = _db()
                try:
                    import uuid
                    new_batch = WasteBatch(
                        batch_id=batch_id.strip() or f"BATCH-{uuid.uuid4().hex[:8].upper()}",
                        source=source or "Unknown",
                        waste_category=waste_type,
                        total_weight_kg=weight_kg,
                        received_date=received_date.isoformat(),
                        status="incoming",
                        notes=notes,
                        created_at=datetime.utcnow(),
                    )
                    db.add(new_batch)
                    db.commit()
                    st.success(f"✅ Batch **{new_batch.batch_id}** registered successfully.")
                except Exception as ex:
                    db.rollback()
                    st.error(f"Registration failed: {ex}")
                finally:
                    db.close()

        section_header("All Batches")
        db = _db()
        try:
            batches = db.query(WasteBatch).order_by(WasteBatch.created_at.desc()).all()
        except Exception as ex:
            st.error(f"Could not load batches: {ex}")
            batches = []
        finally:
            db.close()

        if not batches:
            st.info("No batches registered yet. Use the form above to register incoming e-waste.")
        else:
            for b in batches:
                sb = status_badge(b.status or "unknown", _status_color(b.status or ""))
                with st.expander(f"📦 {b.batch_id} — {b.waste_category} — {b.total_weight_kg} kg  {sb}",
                                 expanded=False):
                    c1, c2, c3 = st.columns(3)
                    c1.markdown(f"**Source:** {b.source}")
                    c1.markdown(f"**Category:** {b.waste_category}")
                    c2.markdown(f"**Weight:** {b.total_weight_kg} kg")
                    c2.markdown(f"**Received:** {b.received_date}")
                    c3.markdown(f"**Status:** {b.status}")
                    if b.notes:
                        st.markdown(f"*Notes:* {b.notes}")
                    # Status update
                    new_status = st.selectbox(
                        "Update Status",
                        ["incoming", "sorting", "dismantling", "processing", "completed", "rejected"],
                        index=["incoming","sorting","dismantling","processing","completed","rejected"].index(
                            b.status or "incoming"),
                        key=f"status_{b.id}",
                    )
                    if st.button("Save Status", key=f"save_{b.id}"):
                        db2 = _db()
                        try:
                            rec = db2.query(WasteBatch).filter(WasteBatch.id == b.id).first()
                            if rec:
                                rec.status = new_status
                                rec.updated_at = datetime.utcnow()
                                db2.commit()
                                st.success("Status updated.")
                                st.rerun()
                        except Exception as ex:
                            db2.rollback()
                            st.error(f"Update failed: {ex}")
                        finally:
                            db2.close()

    # ── TAB 2: DEVICES ─────────────────────────────────────────────────
    with tabs[1]:
        section_header("Device Registry", "Register individual devices within a batch")

        db = _db()
        try:
            batch_options = db.query(WasteBatch).all()
        except Exception:
            batch_options = []
        finally:
            db.close()

        if not batch_options:
            st.info("Register at least one batch before adding devices.")
        else:
            with st.expander("➕ Add Device", expanded=False):
                with st.form("new_device_form"):
                    batch_map = {b.batch_id: b.id for b in batch_options}
                    sel_batch = st.selectbox("Batch", list(batch_map.keys()))
                    c1, c2 = st.columns(2)
                    device_type = c1.selectbox("Device Type", [
                        "laptop", "desktop", "mobile_phone", "tablet", "television",
                        "monitor", "printer", "keyboard", "mouse", "battery_pack",
                        "router", "hard_drive", "other",
                    ])
                    brand = c2.text_input("Brand / Manufacturer")
                    model_name = c1.text_input("Model Name")
                    condition = c2.selectbox("Condition", ["unknown","poor","fair","good","excellent"])
                    weight_kg = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
                    sub = st.form_submit_button("Add Device", type="primary")

                if sub:
                    db3 = _db()
                    try:
                        dev = Device(
                            batch_id=batch_map[sel_batch],
                            device_type=device_type,
                            brand=brand or "Unknown",
                            model_name=model_name or "",
                            condition=condition,
                            weight_kg=weight_kg,
                            created_at=datetime.utcnow(),
                        )
                        db3.add(dev)
                        db3.commit()
                        st.success(f"✅ Device **{device_type}** added to batch {sel_batch}.")
                    except Exception as ex:
                        db3.rollback()
                        st.error(f"Failed: {ex}")
                    finally:
                        db3.close()

            section_header("Device List")
            db4 = _db()
            try:
                devices = db4.query(Device).order_by(Device.created_at.desc()).limit(100).all()
            except Exception as ex:
                st.error(f"Could not load devices: {ex}")
                devices = []
            finally:
                db4.close()

            if not devices:
                st.info("No devices registered yet.")
            else:
                import pandas as pd
                data = [{
                    "ID": d.id,
                    "Batch ID": d.batch_id,
                    "Type": d.device_type,
                    "Brand": d.brand,
                    "Model": d.model_name,
                    "Condition": d.condition,
                    "Weight (kg)": d.weight_kg,
                    "Added": str(d.created_at)[:10] if d.created_at else "",
                } for d in devices]
                st.dataframe(pd.DataFrame(data), use_container_width=True)

    # ── TAB 3: MATERIAL RECOVERY ───────────────────────────────────────
    with tabs[2]:
        section_header("Recovery Records", "Log recovered materials from processed batches")

        db5 = _db()
        try:
            completed_batches = db5.query(WasteBatch).filter(
                WasteBatch.status.in_(["processing","completed"])
            ).all()
        except Exception:
            completed_batches = []
        finally:
            db5.close()

        if not completed_batches:
            st.info("No batches in 'processing' or 'completed' status yet.")
        else:
            with st.expander("➕ Log Recovery Record", expanded=False):
                with st.form("recovery_form"):
                    batch_map2 = {b.batch_id: b.id for b in completed_batches}
                    sel2 = st.selectbox("Batch", list(batch_map2.keys()))
                    c1, c2 = st.columns(2)
                    material = c1.selectbox("Material", [
                        "gold", "silver", "copper", "aluminum", "steel", "iron",
                        "palladium", "platinum", "lithium", "cobalt", "plastic",
                        "glass", "circuit_boards", "other",
                    ])
                    quantity_kg = c2.number_input("Quantity Recovered (kg)", min_value=0.0, step=0.01)
                    purity = c1.number_input("Purity %", 0.0, 100.0, step=0.1)
                    method = c2.selectbox("Recovery Method", [
                        "manual_dismantling", "shredding", "hydrometallurgy",
                        "pyrometallurgy", "electrochemical", "other",
                    ])
                    notes_r = st.text_area("Notes")
                    sub_r = st.form_submit_button("Log Recovery", type="primary")

                if sub_r:
                    db6 = _db()
                    try:
                        rr = RecoveryRecord(
                            batch_id=batch_map2[sel2],
                            material_name=material,
                            quantity_kg=quantity_kg,
                            purity_percent=purity,
                            recovery_method=method,
                            notes=notes_r,
                            source="measured",
                            recorded_at=datetime.utcnow(),
                        )
                        db6.add(rr)
                        db6.commit()
                        st.success(f"✅ Logged {quantity_kg} kg of **{material}** from batch {sel2}.")
                    except Exception as ex:
                        db6.rollback()
                        st.error(f"Failed: {ex}")
                    finally:
                        db6.close()

        section_header("Recovery History")
        db7 = _db()
        try:
            records = db7.query(RecoveryRecord).order_by(RecoveryRecord.recorded_at.desc()).limit(100).all()
        except Exception as ex:
            st.error(f"Could not load records: {ex}")
            records = []
        finally:
            db7.close()

        if not records:
            st.info("No recovery records yet.")
        else:
            import pandas as pd
            data_r = [{
                "Batch": r.batch_id,
                "Material": r.material_name,
                "Qty (kg)": r.quantity_kg,
                "Purity %": r.purity_percent,
                "Method": r.recovery_method,
                "Source": r.source,
                "Date": str(r.recorded_at)[:10] if r.recorded_at else "",
            } for r in records]
            st.dataframe(pd.DataFrame(data_r), use_container_width=True)

            total = sum(r.quantity_kg or 0 for r in records)
            st.metric("Total Material Recovered", f"{total:.2f} kg")

    # ── TAB 4: INVENTORY ───────────────────────────────────────────────
    with tabs[3]:
        section_header("Material Inventory", "Current stock of recovered materials")

        with st.expander("➕ Update Inventory", expanded=False):
            with st.form("inventory_form"):
                c1, c2 = st.columns(2)
                inv_material = c1.selectbox("Material", [
                    "gold", "silver", "copper", "aluminum", "steel", "iron",
                    "palladium", "platinum", "lithium", "cobalt", "plastic",
                    "glass", "circuit_boards", "other",
                ], key="inv_mat")
                inv_qty = c2.number_input("Quantity (kg)", min_value=0.0, step=0.01, key="inv_qty")
                inv_location = c1.text_input("Storage Location", placeholder="e.g. Warehouse A")
                inv_notes = c2.text_area("Notes", key="inv_notes")
                sub_inv = st.form_submit_button("Update Inventory", type="primary")

            if sub_inv:
                db8 = _db()
                try:
                    existing = db8.query(Inventory).filter(
                        Inventory.material_name == inv_material
                    ).first()
                    if existing:
                        existing.quantity_kg = (existing.quantity_kg or 0) + inv_qty
                        existing.location = inv_location or existing.location
                        existing.updated_at = datetime.utcnow()
                    else:
                        inv = Inventory(
                            material_name=inv_material,
                            quantity_kg=inv_qty,
                            location=inv_location,
                            notes=inv_notes,
                            updated_at=datetime.utcnow(),
                        )
                        db8.add(inv)
                    db8.commit()
                    st.success(f"✅ Inventory updated: {inv_material} +{inv_qty} kg")
                except Exception as ex:
                    db8.rollback()
                    st.error(f"Failed: {ex}")
                finally:
                    db8.close()

        section_header("Current Inventory")
        db9 = _db()
        try:
            inventory = db9.query(Inventory).order_by(Inventory.material_name).all()
        except Exception as ex:
            st.error(f"Could not load inventory: {ex}")
            inventory = []
        finally:
            db9.close()

        if not inventory:
            st.info("Inventory is empty. Log recovery records or add stock above.")
        else:
            import pandas as pd
            inv_data = [{
                "Material": i.material_name,
                "Quantity (kg)": i.quantity_kg,
                "Location": i.location or "—",
                "Last Updated": str(i.updated_at)[:10] if i.updated_at else "—",
            } for i in inventory]
            st.dataframe(pd.DataFrame(inv_data), use_container_width=True)

            total_inv = sum(i.quantity_kg or 0 for i in inventory)
            st.metric("Total Inventory", f"{total_inv:.2f} kg")
