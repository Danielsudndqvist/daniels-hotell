document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM fully loaded'); // To check if the script is loading



    // Add event listeners to each button
    moreInfoButtons.forEach(button => {
        button.addEventListener('click', function () {
            console.log('More Info button clicked'); // Log when the button is clicked

            const roomId = this.getAttribute('data-room-id'); // Get the room ID from data attribute
            console.log('Room ID:', roomId); // Log the room ID to confirm it's correct

            // Fetch room details based on roomId
            fetchRoomDetails(roomId);
        });
    });

    // Function to fetch room details via AJAX (fetch API)
    function fetchRoomDetails(roomId) {
        console.log('Fetching details for room ID:', roomId); // Log the room ID being fetched

        fetch(`/room/${roomId}/json/`)
            .then(response => {
                console.log('Response status:', response.status); // Log the response status
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Room data received:', data); // Log the received data
                displayRoomDetails(data); // Display room details in the modal
                
                // Show the modal after data is loaded
                if (roomInfoModal) {
                    roomInfoModal.show(); // Display the modal
                    console.log('Modal displayed');
                } else {
                    console.error('roomInfoModal is not initialized');
                }
            })
            .catch(error => {
                console.error('Error fetching room details:', error); // Log fetch errors
                alert('Failed to fetch room details. Please try again later.');
            });
    }

    // Function to populate the modal with room data
    function displayRoomDetails(data) {
        // Assuming you have elements to populate inside the modal with specific data
        document.getElementById('room-name').innerText = data.name;
        document.getElementById('room-description').innerText = data.description;
        document.getElementById('room-price').innerText = `$${data.price}`;
        document.getElementById('room-capacity').innerText = `${data.capacity} guests`;
        
        // Log that the modal content has been updated
        console.log('Room details populated in modal');
    }
});
