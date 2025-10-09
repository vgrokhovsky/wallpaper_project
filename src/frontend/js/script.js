document.addEventListener('DOMContentLoaded', () => {
    // Загрузка обоев из API
    fetchWallpapers();

    // Делегирование событий для кликов по изображениям
    document.getElementById('wallpapers-container').addEventListener('click', (e) => {
        if (e.target.classList.contains('wallpaper-item-img')) {
            const imageSrc = e.target.getAttribute('src').replace('../', ''); // Убираем ../ для openFullScreen
            console.log('Clicked image:', imageSrc); // Отладка
            openFullScreen(imageSrc);
        }
    });

    const categoryLinks = document.querySelectorAll('.category-list a');
    // console.log('categoryLinks', categoryLinks)
    categoryLinks.forEach(link => {
        // console.log(link.getAttribute('data-category'));
        link.addEventListener('click', (e) => {
            // console.log(e)
            const category = e.target.getAttribute('data-category');
            // console.log(category)
            fetchWallpapers(category)
        })
    });

    // // Добавление обработчика событий для фильтра ориентации
    // document.getElementById('orientation').addEventListener('change', (e) => {
    //     const orientation = e.target.value;
    //     console.log(`Фильтр по ориентации: ${orientation}`);
    //     // Реализация фильтрации по ориентации (добавить позже)
    // });

    // Закрытие полноэкранного режима при клике за пределами изображения
    document.getElementById('fullscreen-box').addEventListener('click', (e) => {
        if (e.target.classList.contains('fullscreen-box-bg')) {
            toggleFullScreen();
        }
    });
});

async function fetchWallpapers(category = null) {
    const orientation = document.getElementById('orientation').value;
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (orientation) params.append('orientation', orientation);
    const response = await fetch(
        `http://127.0.0.1:5000/api/wallpapers?${params.toString()}`);

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json()
    console.log(data)

    // fetch('http://127.0.0.1:5000/api/wallpapers')
    //     .then(response => {
    //         if (!response.ok) {
    //             throw new Error(`HTTP error! status: ${response.status}`);
    //         }
    //         return response.json();
    //     })
    //     .then(data => {
    //         if (data.error) {
    //             console.error('Ошибка при загрузке обоев:', data.error);
    //             return;
    //         }
    //         const container = document.getElementById('wallpapers-container');
    //         container.innerHTML = ''; // Очистка содержимого
    //         data.wallpapers.forEach(wallpaper => {
    //             const item = document.createElement('div');
    //             item.className = 'wallpaper-item';
    //             const imagePath = wallpaper.startsWith('wallpapers/') ? wallpaper : `wallpapers/${wallpaper}`;
    //             item.innerHTML = `
    //                 <img class="wallpaper-item-img" src="../${imagePath}" alt="Обои">
    //                 <div class="wallpaper-menu"></div>
    //             `;
    //             container.appendChild(item);
    //         });
    //     })
    //     .catch(error => console.error('Ошибка запроса:', error));
}

function openFullScreen(imageSrc) {
    const fullscreenBox = document.getElementById('fullscreen-box');
    const fullscreenImage = document.getElementById('fullscreen-image');
    const imagePath = imageSrc.startsWith('wallpapers/') ? imageSrc : `wallpapers/${imageSrc}`;
    fullscreenImage.src = `../${imagePath}`;
    console.log('Opening fullscreen image:', fullscreenImage.src); // Отладка
    fullscreenBox.style.display = 'block';
}

function toggleFullScreen() {
    const fullscreenBox = document.getElementById('fullscreen-box');
    fullscreenBox.style.display = 'none';
}

function downloadImage() {
    const imageSrc = document.getElementById('fullscreen-image').src;
    const link = document.createElement('a');
    link.href = imageSrc;
    link.download = imageSrc.split('/').pop();
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}