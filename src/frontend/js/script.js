console.log('JS console start');
const content = document.querySelector('#content');

// fetch('http://127.0.0.1:5000/api/get_data/', {
//     method: 'GET',
//     headers: {
//         'Content-Type': 'application/json'
//     }
// })
//     .then(response => {
//         if (!response.ok) {
//             throw new Error(`Ошибка HTTP: ${response.status}`);
//         }
//         return response.json();
//     })
//     .then(data => {
//         console.log('Данные от API:', data);
//         content.innerText = data.message;
//     })
//     .catch(error => {
//         console.error('Ошибка:', error);
//         content.innerText = 'Произошла ошибка при запросе';
//     });

async function fetchData() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/get_data/', {
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
        content.innerText = data.message;
    } catch (error) {
        console.error('Ошибка:', error);
        content.innerText = 'Произошла ошибка при запросе';
    }
}
