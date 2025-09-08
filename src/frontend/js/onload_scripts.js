window.onload = function () {
    const width = window.screen.width
    const height = window.screen.height
    console.log(width, height)
};

function openFullScreenBox() {
    console.log('openFullScreenBox start')
    const images = document.querySelectorAll('.wallpaper-item-img');
    const imgBox = document.querySelector('.fullscreen-box');
    const imgItem = document.querySelector('.fullscreen-image-item');
    if (images.length > 0) {
        images.forEach(img => {
            img.addEventListener('click', function () {
                const src = this.getAttribute('src');
                imgBox.style.visibility = 'visible'
                imgItem.setAttribute('src', src)
                console.log('click:', src)
                return src
            })
        })
    }
}

