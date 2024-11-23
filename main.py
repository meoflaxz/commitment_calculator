import streamlit as st
import pandas as pd

def get_pastel_color(value, max_value):
    return f'background-color: rgba(173, 216, 230, {value/max_value:.2f})'

def get_emoji_for_commitment(name):
    emoji_map = {
        'Rumah Sewa': '🏠', 'Ninja': '🏍️', 'ASB Saving': '💰',
        'ASBF': '🏦', 'Insurance': '🛡️', 'S24 Ultra': '📱',
        'Tabung Haji': '🕌', 'Telephone': '☎️', 'Microsoft': '💻',
        'Parents': '👨‍👩‍👦', 'Shopee': '🛒', 'Google Storage': '☁️',
        'Siblings': '👥', 'Makan': '🍽️', 'TNG': '💳',
        'Foodpanda': '🐼', 'DigitalOcean': '🌊', 'Claude': '🤖'
    }
    return emoji_map.get(name, '💸')

def calculate_commitments():
    if 'commitments' not in st.session_state:
        st.session_state.commitments = [
            ('Rumah Sewa', 938.0), ('Ninja', 290.0),
            ('ASB Saving', 300.0), ('ASBF', 158.0),
            ('Insurance', 217.0), ('S24 Ultra', 0.0),
            ('Tabung Haji', 50.0), ('Telephone', 49.0),
            ('Microsoft', 10.0), ('Parents', 50.0),
            ('Shopee', 0.0), ('Google Storage', 97.99),
            ('Siblings', 100.0), ('Makan', 900.0),
            ('TNG', 20.0), ('Foodpanda', 6.5),
            ('DigitalOcean', 26.0), ('Claude', 88.0)
        ]

    st.set_page_config(layout="wide")
    st.markdown("<h1 style='text-align: center;'>💰 Monthly Commitment Calculator 💰</h1>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["💼 Main", "📊 Analysis"])

    with tab1:
        # Create three columns with the middle one for content
        left_spacer, main_content, right_spacer = st.columns([1, 2, 1])
        
        with main_content:
            # Income Section
            col1, col2 = st.columns(2)
            with col1:
                salary = st.number_input('Gaji Baru 💵', value=4030.0)
            with col2:
                kwsp = salary * 0.11
                st.number_input('KWSP (11%) 📊', value=float(kwsp), disabled=True)
            net_salary = salary - kwsp

            # Calculate commitments
            commitments = dict(st.session_state.commitments)
            total_commitments = sum(commitments.values())
            balance = net_salary - total_commitments

            # Summary Section
            st.markdown("<h2 style='text-align: center;'>📊 Summary</h2>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric('Net Salary 💵', f'RM {net_salary:.2f}')
            with col2:
                st.metric('Total Commitments 💳', f'RM {total_commitments:.2f}')
            with col3:
                st.metric('Balance 💰', f'RM {balance:.2f}')

            # Ratio visualization
            st.markdown("<h3 style='text-align: center;'>Salary Distribution</h3>", unsafe_allow_html=True)
            balance_ratio = (balance / net_salary) * 100
            commitment_ratio = (total_commitments / net_salary) * 100
            st.progress(commitment_ratio/100)
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"💳 Commitments: {commitment_ratio:.1f}%")
            with col2:
                st.write(f"💰 Balance: {balance_ratio:.1f}%")

            # Fixed Commitments Section
            st.markdown("<h2 style='text-align: center;'>📝 Fixed Commitments</h2>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            updated_commitments = {}

            # Initialize commitment_types
            if 'commitment_types' not in st.session_state:
                st.session_state.commitment_types = {name: 'fixed' for name, _ in [
                    ('Rumah Sewa', 0), ('Ninja', 0), ('Insurance', 0),
                    ('S24 Ultra', 0), ('Telephone', 0), ('Microsoft', 0),
                    ('Google Storage', 0), ('Parents', 0), ('Siblings', 0),
                    ('DigitalOcean', 0), ('Claude', 0)
                ]}

            for i, (name, amount) in enumerate(st.session_state.commitments):
                emoji = get_emoji_for_commitment(name)
                is_fixed = st.session_state.commitment_types.get(name, 'flexible') == 'fixed'
                bg_color = "#ffd6d6" if is_fixed else "#d6ffd6"

                # Create a single row with number input and button side by side
                st.markdown(
                    f"""
                    <div style="background-color: {bg_color}; padding: 10px; border-radius: 5px; margin: 5px 0; display: flex; align-items: center; justify-content: space-between; font-size: 0.8rem !important">
                        <div>{emoji} {name}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Display in one row without nesting
                number_col, button_col = st.columns([1, 4])  # Adjust proportions as needed
                with button_col:
                    updated_commitments[f"{emoji} {name}"] = st.number_input(
                        label=f"Amount for {name}",
                        value=float(amount),
                        label_visibility="collapsed",
                        key=f"input_{name}"
                    )
                with number_col:
                    if st.button("🔄", key=f"toggle_{name}", help="Toggle fixed/flexible"):
                        if name in st.session_state.commitment_types:
                            del st.session_state.commitment_types[name]
                        else:
                            st.session_state.commitment_types[name] = 'fixed'
                        st.rerun()

                    

                st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        # Create three columns with the middle one for content
        left_spacer, analysis_content, right_spacer = st.columns([1, 2, 1])
        
        with analysis_content:
            # Commitment Breakdown
            st.markdown("<h2 style='text-align: center;'>📊 Commitment Breakdown</h2>", unsafe_allow_html=True)
            df = pd.DataFrame(list(updated_commitments.items()), columns=['Item', 'Amount'])
            df = df.sort_values('Amount', ascending=False)
            df['Percentage'] = (df['Amount'] / total_commitments * 100).round(2)
            
            max_amount = df['Amount'].max()
            st.dataframe(
                df.style.format({'Amount': 'RM {:.2f}', 'Percentage': '{:.2f}%'})
                      .apply(lambda x: [get_pastel_color(v, max_amount) for v in x], subset=['Amount']),
                use_container_width=True
            )
            
            # Distribution Chart
            st.markdown("<h2 style='text-align: center;'>📈 Commitment Distribution</h2>", unsafe_allow_html=True)
            st.bar_chart(df.set_index('Item')['Amount'])

    # Sidebar for managing commitments
    st.sidebar.markdown("<h3 style='text-align: center;'>✨ Manage Commitments ✨</h3>", unsafe_allow_html=True)
    new_commitment_name = st.sidebar.text_input("New Commitment Name")
    new_commitment_amount = st.sidebar.number_input("Amount", min_value=0.0)
    if st.sidebar.button("➕ Add Commitment"):
        if new_commitment_name and new_commitment_amount >= 0:
            st.session_state.commitments.append((new_commitment_name, new_commitment_amount))
            st.sidebar.success("Added successfully! ✅")

    commitment_names = [name for name, _ in st.session_state.commitments]
    to_delete = st.sidebar.selectbox("Select commitment to delete", commitment_names)
    if st.sidebar.button("❌ Delete Commitment"):
        st.session_state.commitments = [(name, amount) for name, amount in st.session_state.commitments if name != to_delete]
        st.sidebar.success(f"Deleted {to_delete} ✅")

    st.session_state.commitments = [(name.split(' ', 1)[1], amount) for name, amount in updated_commitments.items()]

if __name__ == '__main__':
    calculate_commitments()