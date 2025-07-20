import streamlit as st

# Настройка Streamlit
st.title("Центр поддержки пользователей")

# Инициализация сессионного состояния для хранения истории чата
if "message" not in st.session_state:
    st.session_state.message = []

# Функция для отображения сообщений
for messag in st.session_state.message:
    with st.chat_message(messag["role"]):
        st.markdown(messag["content"])

# Ввод пользователя
prompt = st.chat_input("Введите ваше сообщение")
file = open('answers.txt', 'a')
file.write(str(prompt))
file.close()
if prompt:
    # Добавление сообщения пользователя в историю чата
    st.session_state.message.append({"role": "user", "content": prompt})
    # Отображение сообщения пользователя
    with st.chat_message("user"):
        st.markdown(prompt+"     ")

    response = "Здравсвуйте, мы примем ваш вопрос к сведению, позже представитель ЦПП свяжется с вами. Также вы можете обратиться в ЦПП компании YADRO по ссылке: https://sp.yadro.com/programms/"
    # Добавление ответа модели в историю чата
    st.session_state.message.append({"role": "assistant", "content": response})
    # Отображение ответа модели
    with st.chat_message("assistant"):
        st.markdown(response)


