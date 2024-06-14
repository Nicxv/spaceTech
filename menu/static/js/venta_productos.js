let map;
let marker;
let autocomplete;
let geocoder;
let precioEnvioAñadido = false;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -33.4489, lng: -70.6693},  // Santiago, Chile
        zoom: 12
    });

    marker = new google.maps.Marker({
        map: map,
        draggable: true
    });

    geocoder = new google.maps.Geocoder();

    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('direccion'),
        {
            types: ['geocode'],
            componentRestrictions: {country: 'cl'}
        }
    );

    autocomplete.addListener('place_changed', onPlaceChanged);

    map.addListener('click', (e) => {
        placeMarkerAndPanTo(e.latLng, map);
    });

    marker.addListener('dragend', (e) => {
        geocodePosition(marker.getPosition());
    });

    // Set initial position if there is a value in the address field
    const initialAddress = document.getElementById('direccion').value;
    if (initialAddress) {
        geocodeAddress(initialAddress);
    }
}

function onPlaceChanged() {
    let place = autocomplete.getPlace();
    if (!place.geometry) {
        window.alert("No details available for input: '" + place.name + "'");
        return;
    }

    map.setCenter(place.geometry.location);
    map.setZoom(17);

    marker.setPosition(place.geometry.location);
    document.getElementById('direccion').value = place.formatted_address;
}

function placeMarkerAndPanTo(latLng, map) {
    marker.setPosition(latLng);
    map.panTo(latLng);
    geocodePosition(latLng);
}

function geocodePosition(pos) {
    geocoder.geocode({
        location: pos
    }, (results, status) => {
        if (status === 'OK') {
            if (results[0]) {
                document.getElementById('direccion').value = results[0].formatted_address;
            } else {
                window.alert('No results found');
            }
        } else {
            window.alert('Geocoder failed due to: ' + status);
        }
    });
}

function geocodeAddress(address) {
    geocoder.geocode({ 'address': address }, function(results, status) {
        if (status === 'OK') {
            map.setCenter(results[0].geometry.location);
            marker.setPosition(results[0].geometry.location);
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('retiro_local').addEventListener('change', toggleDeliveryOption);
    document.getElementById('envio_domicilio').addEventListener('change', toggleDeliveryOption);

    document.getElementById('guardar_direccion').addEventListener('click', confirmarDireccion);

    document.getElementById('cambiar_fecha').addEventListener('click', mostrarOpcionesFecha);
    document.getElementById('confirmar_fecha').addEventListener('click', confirmarFecha);

    // Trigger initial toggle to show the correct address field
    toggleDeliveryOption();

    // Initialize Flatpickr on the date input field with minDate set to 3 days from today
    flatpickr("#fecha_entrega", {
        minDate: new Date().fp_incr(3),
        dateFormat: "Y-m-d",
    });
});

function toggleDeliveryOption() {
    let retiroLocalChecked = document.getElementById('retiro_local').checked;
    let envioDomicilioChecked = document.getElementById('envio_domicilio').checked;

    document.getElementById('direccion_local').style.display = retiroLocalChecked ? 'block' : 'none';
    document.getElementById('direccion_cliente').style.display = envioDomicilioChecked ? 'block' : 'none';
}

function confirmarDireccion() {
    Swal.fire({
        title: 'Confirmar Dirección',
        text: "Si confirma su dirección no podrá volver a cambiarla",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Confirmar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            guardarDireccion();
        }
    });
}

function guardarDireccion() {
    const direccion = document.getElementById('direccion').value;
    fetch('/guardar_direccion/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ direccion: direccion })
    }).then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            document.getElementById('precio_envio').innerText = `Precio de envío: ${formatPrice(data.precio_envio)}`;
            actualizarTotal(data.precio_envio);
            document.getElementById('map').style.display = 'none';
            document.getElementById('guardar_direccion').style.display = 'none';
            document.getElementById('direccion').disabled = true;  // Deshabilitar el campo de dirección
            alert('Dirección guardada correctamente');
        } else {
            alert('Error al guardar la dirección: ' + data.message);
        }
    }).catch(error => {
        console.error('Error:', error);
        alert('Error al guardar la dirección');
    });
}

function formatPrice(price) {
    return new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP' }).format(price);
}

function actualizarTotal(precioEnvio) {
    if (!precioEnvioAñadido) {
        const totalElement = document.querySelector('.total');
        let total = parseFloat(totalElement.dataset.total);
        total += precioEnvio;
        totalElement.innerText = `Total: ${formatPrice(total)}`;
        totalElement.dataset.total = total;
        precioEnvioAñadido = true;
    }
}

function mostrarOpcionesFecha() {
    document.querySelector('.date-options').style.display = 'block';
    document.getElementById('cambiar_fecha').style.display = 'none';
}

function confirmarFecha() {
    const fechaEntrega = document.getElementById('fecha_entrega').value;
    if (fechaEntrega) {
        document.getElementById('fecha_entrega_seleccionada').innerText = fechaEntrega;
        document.querySelector('.date-options').style.display = 'none';
        document.getElementById('cambiar_fecha').style.display = 'block';
    } else {
        alert('Por favor, selecciona una fecha de entrega.');
    }
}