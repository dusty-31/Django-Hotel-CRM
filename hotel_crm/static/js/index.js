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

function selectCheckIn(event) {
    if (event.target.value !== '') {
        let checkOutInput = window.document.getElementById('check_out');
        if (checkOutInput.value !== '' && event.target.value > checkOutInput.value) {
            alert("Check-in date cannot be after check-out date!");
            removeQueryParam('check_in');
            return;
        }
        addQueryParam('check_in', event.target.value);
    } else {
        removeQueryParam('check_in');
    }
}

function selectCheckOut(event) {
    if (event.target.value !== '') {
        let checkInInput = window.document.getElementById('check_in');
        if (checkInInput.value !== '' && event.target.value < checkInInput.value) {
            alert("Check-out date cannot be before check-in date!");
            removeQueryParam('check_out');
            return;
        }
        addQueryParam('check_out', event.target.value);
    } else {
        removeQueryParam('check_out');
    }
}

function selectNumberOfGuest(event) {
    if (event.target.value !== '') {
        addQueryParam('number_of_guests', event.target.value);
    } else {
        removeQueryParam('number_of_guests');
    }
}

window.document.getElementById('hotel_choice').addEventListener('change', selectHotel);
window.document.getElementById('check_in').addEventListener('change', selectCheckIn);
window.document.getElementById('check_out').addEventListener('change', selectCheckOut);
window.document.getElementById('number_of_guests').addEventListener('input', selectNumberOfGuest);
