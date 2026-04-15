import streamlit as st
import database as db
import firewall_logic as fl

st.set_page_config(page_title="PyWall Architect", layout="wide")
db.init_db()

st.title("🛡️ PyWall Architect - Firewall Rule Generator")

col1, col2 = st.columns(2)

with col1:
    st.header("Configura Nuova Regola")
    rule_name = st.text_input("Nome Regola (es. Allow HTTP)")
    proto = st.selectbox("Protocollo", ["TCP", "UDP", "ICMP"])
    port = st.number_input("Porta Destinazione", min_value=1, max_value=65535, value=80)
    source = st.text_input("IP Sorgente (es. 192.168.1.0/24 o vuoto per ANY)", "0.0.0.0/0")
    action = st.radio("Azione", ["ACCEPT", "DROP", "REJECT"])
    target = st.selectbox("Target System", ["iptables", "nftables", "Cisco ASA"])

    if st.button("Salva e Genera", type="primary"):
        syntax = fl.generate_rule(proto, port, source, action, target)
        if "Errore" not in syntax:
            db.save_rule(rule_name, proto, port, source, action, target)
            st.success(f"Regola '{rule_name}' salvata!")
        st.code(syntax, language='bash')

with col2:
    st.header("Regole Recenti")
    rules = db.get_all_rules()[:10]
    for rule in rules:
        with st.expander(f"{rule['name']} ({rule['target_system']})"):
            syntax = fl.generate_rule(rule['protocol'], rule['port'], rule['source_ip'], rule['action'], rule['target_system'])
            st.code(syntax, language='bash')
            if st.button(f"Elimina", key=f"del_{rule['id']}"):
                db.delete_rule(rule['id'])
                st.rerun()

st.divider()
st.header("📋 Tutte le Regole Archiviate")
all_rules = db.get_all_rules()
if all_rules:
    st.dataframe(all_rules, use_container_width=True)
else:
    st.info("Nessuna regola salvata.")