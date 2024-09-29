document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM fully loaded');

    // Function to fetch room details via AJAX (fetch API)
    function fetchRoomDetails(roomId) {
        console.log('Fetching details for room ID:', roomId);

        fetch(`/room/${roomId}/json/`)
            .then(response => {
                console.log('Response status:', response.status);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Room data received:', data);
                displayRoomDetails(data);
            })
            .catch(error => {
                console.error('Error fetching room details:', error);
                alert('Failed to fetch room details. Please try again later.');
            });
    }

    // Function to populate the modal with room data
    function displayRoomDetails(data) {
        document.getElementById('room-name').innerText = data.name;
        document.getElementById('room-description').innerText = data.description;
        document.getElementById('room-price').innerText = `$${data.price}`;
        document.getElementById('room-capacity').innerText = `${data.max_occupancy} guests`;
        console.log('Room details populated in modal');
    }
});