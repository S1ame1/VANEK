import streamlit as st
import requests


# Функция для отправки запроса к модели Langflow
def query_langflow_model(message):
    api_key = "sk-z9pNBz1c36vVMv5ZnkwgjJJ3GbKXqMCiMlnKGUE6vHI"
    url = "http://localhost:7860/api/v1/run/51437b11-074d-4b87-bfbd-487b4a302d6f"  # The complete API endpoint URL for this flow
    # Request payload configuration
    payload = {
        "output_type": "chat",
        "input_type": "chat",
        "input_value": message
    }
    # Request headers
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key  # Authentication key from environment variable
    }
    # Send API request
    response = requests.request("POST", url, json=payload, headers=headers)
    response.raise_for_status()  # Raise exception for bad status codes
    data = response.json()
    return data["outputs"][0]["outputs"][0]["artifacts"]["message"]


# Настройка страницы
st.set_page_config(
    page_title="Tatlin Assistant",
    page_icon="🤖",
    layout="centered"
)

# Кастомные стили CSS для тёмной темы
st.markdown("""
<style>
    /* Основные стили */
    .stApp {
        background-color: #0e0e0e;
        color: #ffffff;
    }
    .main-title {
        font-size: 1.8rem !important;
        color: #ffffff !important;
        text-align: center;
        margin-bottom: 1rem;
    }
    .welcome-card {
        background: #1a1a1a;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(255, 255, 255, 0.05);
        margin: 0 auto;
        max-width: 500px;
        border: 1px solid #2a2a2a;
    }
    .styled-button {
        background-color: #6200ee !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 10px 24px !important;
        font-size: 0.9rem !important;
        transition: all 0.3s !important;
    }
    .styled-button:hover {
        background-color: #3700b3 !important;
        transform: scale(1.02);
    }
    .back-button {
        background-color: #333 !important;
    }
    .avatar-large {
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        padding: 1rem;
        font-size: 0.8rem;
        color: #aaa;
    }
    .divider {
        height: 1px;
        background: linear-gradient(to right, transparent, #444, transparent);
        margin: 1rem 0;
    }
    /* Стили для модального окна */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.7);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }
    .modal-content {
        background-color: #1a1a1a;
        padding: 2rem;
        border-radius: 12px;
        max-width: 500px;
        width: 80%;
        border: 1px solid #2a2a2a;
        text-align: center;
    }
    /* Компактные элементы */
    .stTextInput>div>div>input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #444 !important;
        padding: 8px 12px !important;
    }
    /* Анимации */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeIn 0.3s ease-out;
    }
    /* Стили для чата */
    .chat-container {
        max-height: 60vh;
        overflow-y: auto;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 12px;
        background-color: #1a1a1a;
        border: 1px solid #2a2a2a;
    }
</style>
""", unsafe_allow_html=True)

# Инициализация состояний сессии
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'show_support' not in st.session_state:
    st.session_state.show_support = False
if "messages" not in st.session_state:
    st.session_state.messages = []


# Функция для отображения модального окна поддержки
def support_modal():
    if st.session_state.show_support:
        st.markdown("""
        <div class="modal-overlay">
            <div class="modal-content fade-in">
                <h3>Служба поддержки</h3>
                <div style="margin: 1.5rem 0;">
                    <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">solution_team@datatech.ru</p>
                    <p style="font-size: 1.1rem;">+7 (495) 123-45-67</p>
                </div>
                <button onclick="window.parent.document.querySelector('section.main').firstElementChild.click()" 
                        style="background-color: #6200ee; color: white; border: none; border-radius: 20px; padding: 10px 24px; cursor: pointer; margin-top: 1rem;">
                    Вернуться назад
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)


# Главный контейнер для динамического контента
main_container = st.container()

with main_container:
    support_modal()  # Всегда проверяем, нужно ли показывать модальное окно

    if not st.session_state.show_support:
        if not st.session_state.submitted:
            # Форма знакомства
            st.markdown('<div class="avatar-large">👋</div>', unsafe_allow_html=True)
            st.markdown('<h1 class="main-title">Tatlin Assistant</h1>', unsafe_allow_html=True)

            with st.container():
                with st.form("intro_form"):
                    user_name = st.text_input("Как вас зовут?", placeholder="Ваше имя...")

                    submitted = st.form_submit_button(
                        "Продолжить →",
                        use_container_width=True,
                        type="primary"
                    )

                    if submitted:
                        if user_name:
                            st.session_state.submitted = True
                            st.session_state.user_name = user_name
                            st.rerun()
                        else:
                            st.warning("Пожалуйста, введите ваше имя")

        elif st.session_state.submitted:
            # Чат-интерфейс
            st.markdown(f'<h1 class="main-title">Чат с Tatlin Assistant</h1>', unsafe_allow_html=True)

            # Контейнер для чата
            chat_container = st.container()

            with chat_container:
                # Отображение приветственного сообщения
                if len(st.session_state.messages) == 0:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Привет, {st.session_state.user_name}! Чем я могу вам помочь?"
                    })

                # Отображение истории чата
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

            # Ввод пользователя
            st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
            prompt = st.chat_input("Введите ваше сообщение")
            st.markdown('</div>', unsafe_allow_html=True)
            if prompt:
                # Добавление сообщения пользователя в историю чата
                st.session_state.messages.append({"role": "user", "content": prompt})

                # Получение ответа от модели Langflow
                response = query_langflow_model(prompt)

                # Добавление ответа модели в историю чата
                st.session_state.messages.append({"role": "assistant", "content": response})

                # Перезагрузка страницы для отображения новых сообщений
                st.rerun()

            # Кнопка "Изменить имя"
            if st.button(
                    "Изменить имя ↩️",
                    use_container_width=True,
                    key="back_to_start"
            ):
                st.session_state.submitted = False
                st.session_state.messages = []
                st.rerun()



