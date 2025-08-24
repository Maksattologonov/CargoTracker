// Утилиты для работы с Telegram авторизацией

class TelegramAuth {
    constructor(botName, callbackUrl = null) {
        this.botName = botName;
        this.callbackUrl = callbackUrl;
    }

    // Инициализация виджета программно
    initWidget(containerId, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const script = document.createElement('script');
        script.async = true;
        script.src = 'https://telegram.org/js/telegram-widget.js?22';
        script.setAttribute('data-telegram-login', this.botName);
        script.setAttribute('data-size', options.size || 'large');
        script.setAttribute('data-corner-radius', options.cornerRadius || '10');

        if (options.hideUserPhoto) {
            script.setAttribute('data-userpic', 'false');
        }

        if (this.callbackUrl) {
            script.setAttribute('data-auth-url', this.callbackUrl);
        } else {
            script.setAttribute('data-onauth', 'onTelegramAuth(user)');
        }

        if (options.requestAccess) {
            script.setAttribute('data-request-access', 'write');
        }

        container.appendChild(script);
    }

    // Ручная авторизация через popup
    openAuthPopup() {
        const authUrl = `https://oauth.telegram.org/auth?bot_id=${this.botName}&origin=${encodeURIComponent(window.location.origin)}&return_to=${encodeURIComponent(window.location.href)}`;

        const popup = window.open(
            authUrl,
            'telegram-auth',
            'width=400,height=500,scrollbars=yes,resizable=yes'
        );

        return new Promise((resolve, reject) => {
            const checkClosed = setInterval(() => {
                if (popup.closed) {
                    clearInterval(checkClosed);
                    reject(new Error('Popup closed'));
                }
            }, 1000);

            const messageHandler = (event) => {
                if (event.origin === 'https://oauth.telegram.org') {
                    clearInterval(checkClosed);
                    popup.close();
                    window.removeEventListener('message', messageHandler);

                    if (event.data && event.data.user) {
                        resolve(event.data.user);
                    } else {
                        reject(new Error('No user data received'));
                    }
                }
            };

            window.addEventListener('message', messageHandler);
        });
    }

    // Проверка валидности данных (клиентская сторона)
    validateAuthData(authData) {
        const required = ['id', 'first_name', 'auth_date', 'hash'];
        return required.every(field => authData.hasOwnProperty(field));
    }

    // Отправка данных на сервер
    async sendToServer(authData, endpoint = '/telegram-callback/') {
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify(authData)
            });

            return await response.json();
        } catch (error) {
            console.error('Server request failed:', error);
            throw error;
        }
    }

    // Получение CSRF токена
    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }
}

// Глобальная инициализация
window.TelegramAuth = TelegramAuth;
