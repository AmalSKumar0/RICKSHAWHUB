// Get modal element
var modal = document.getElementById('reviewModal');

// Get the button that opens the modal
var btn = document.getElementById('openModalBtn');

// Get the <span> element that closes the modal
var closeBtn = document.getElementsByClassName('close')[0];

// Function to open the modal
btn.onclick = function() {
    modal.style.display = 'block';
    
    // Reset animations by reflowing the review items
    var reviewItems = document.querySelectorAll('.review-item');
    reviewItems.forEach(function(item) {
        item.classList.remove('slide-in');
        void item.offsetWidth; // Trigger reflow
        item.classList.add('slide-in');
    });
}

// Function to close the modal
closeBtn.onclick = function() {
    modal.style.display = 'none';
}

// Close the modal when clicking outside of the modal content
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}
btn.onclick = function() {
    modal.style.display = 'block';
    
    var reviewItems = document.querySelectorAll('.review-item');
    reviewItems.forEach(function(item, index) {
        item.style.opacity = '0';
        item.style.transform = 'translateX(-50px)';
        item.style.animation = `slideIn 0.5s forwards`;
        item.style.animationDelay = `${index * 0.2}s`;
    });
}
