$(document).ready(function() {
    $('#ask-btn').click(function() {
        const question = $('#question').val();

        if (!question.trim()) {
            // Show error if the question input is empty
            $('#answer').text('Please enter a question.');
            return;
        }

        // AJAX call to Flask backend
        $.ajax({
            url: '/ask',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ question: question }),
            success: function(response) {
                // Display the AI's answer
                $('#answer').text(response.answer);

                // Update the history section dynamically
                $('#history').prepend(`<li class="list-group-item"><strong>Q:</strong> ${question} <br><strong>A:</strong> ${response.answer}</li>`);
                
                // Clear the input field after submitting
                $('#question').val('');
            },
            error: function(xhr, status, error) {
                // Handle errors
                console.log(error);
                $('#answer').text('An error occurred. Please try again.');
            }
        });
    });
});
