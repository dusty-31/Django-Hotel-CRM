function addQueryParam(key, value) {
    let url = new URL(window.location.href);
    let params = new URLSearchParams(url.search);
    params.set(key, value);
    url.search = params.toString();
    window.location.href = url.toString();
}

function removeQueryParam(key) {
    let url = new URL(window.location.href);
    let params = new URLSearchParams(url.search);
    params.delete(key);
    url.search = params.toString();
    window.location.href = url.toString();
}

function selectHotel(event) {
    if (event.target.value !== '') {
        addQueryParam('hotel_id', event.target.value);
    } else {
        removeQueryParam('hotel_id');
    }
}

window.document.getElementById('hotel_choice').addEventListener('change', selectHotel);
