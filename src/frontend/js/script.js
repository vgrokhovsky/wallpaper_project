console.log('JS console start');

async function fetchData(url, content_name) {
    const content = document.querySelector(content_name);
    if (!content) {
        console.error(`Элемент ${content_name} не найден`);
        return;
    }
    try {
        content.innerText = 'Загружаю данные...';
        const response = await fetch(`http://127.0.0.1:5000/api/${url}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }
        const data = await response.json();
        console.log('Данные от API:', data);
        content.innerText = `Ответ от сервера: ${data.message}`;
    } catch (error) {
        console.error('Ошибка:', error);
        content.innerText = `Ошибка: ${error.message}`;
    }
}


function toggleDisplay() {
    const elementBOX = document.querySelector('.fullscreen-box');
    const elementBg = document.querySelector('.fullscreen-box-bg');
    if (elementBg) {
        elementBg.addEventListener('click', function () {
            console.log('hidden')
            elementBOX.style.visibility = 'hidden'
        })
    }
}

