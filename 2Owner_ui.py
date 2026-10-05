import os
import streamlit as st
import database as db

st.header("Owner Page")

# optional password: set OWNER_PASSWORD in .env to enable
pw = os.getenv("OWNER_PASSWORD")
if pw and not st.session_state.get("ok"):
    if st.text_input("Owner password", type="password") == pw:
        st.session_state.ok = True
        st.rerun()
    st.stop()

work = st.selectbox("Choose option", ["Get Business", "Get Products", "Get Product_by_name",
                                      "Add Product", "Update Product"],
                    index=None, placeholder="Choose")


def product_fields(prefix, row=None):
    """Builds the input form automatically from the products table structure."""
    out = {}
    for c in db.columns("products"):
        name, typ = c["Field"], c["Type"].lower()
        if "auto_increment" in c["Extra"]:
            continue
        old, key = (row or {}).get(name), f"{prefix}_{name}"
        if "tinyint(1)" in typ or "bool" in typ:
            out[name] = int(st.checkbox(name, value=bool(old), key=key))
        elif "int" in typ:
            out[name] = st.number_input(name, step=1, value=int(old or 0), key=key)
        elif any(t in typ for t in ("decimal", "float", "double")):
            out[name] = st.number_input(name, step=1.0, value=float(old or 0), key=key)
        elif "text" in typ:
            out[name] = st.text_area(name, value=str(old or ""), key=key)
        else:
            out[name] = st.text_input(name, value=str(old or ""), key=key)
    return out


if work == "Get Business":
    st.dataframe(db.get_business(), hide_index=True)

elif work == "Get Products":
    st.dataframe(db.get_products(), hide_index=True)

elif work == "Get Product_by_name":
    q = st.text_input("Search")
    if q:
        hits = [r for r in db.get_products() if q.lower() in " ".join(map(str, r.values())).lower()]
        st.dataframe(hits, hide_index=True) if hits else st.warning("No product found.")

elif work == "Add Product":
    with st.form("add", clear_on_submit=True):
        data = product_fields("add")
        if st.form_submit_button("Add product"):
            try:
                db.add_product(data)
                st.success("Product added.")
            except Exception as e:
                st.error(e)

elif work == "Update Product":
    rows, pk = db.get_products(), db.primary_key()
    if not rows:
        st.info("No products.")
    else:
        i = st.selectbox("Select product", range(len(rows)),
                         format_func=lambda i: " - ".join(str(v) for v in list(rows[i].values())[:2]))
        with st.form(f"upd{i}"):
            data = product_fields(f"upd{i}", rows[i])
            if st.form_submit_button("Update"):
                try:
                    db.update_product(pk, rows[i][pk], data)
                    st.success("Updated.")
                    st.rerun()
                except Exception as e:
                    st.error(e)