let logBox = null;
$(document).ready(function () {
    $('#btnSubmit').click(function () {
        logBox = $('.message-box');
        const dir_url = $('#dir_url').val();
        console.log(dir_url);
        $.post("/extract",
        {
            dir_url: dir_url
        },
        function(data){
            console.log(data)
        });
        logBox.empty();
        posts()
    })
});
function posts() {
    console.log('posts');
    $.post('/update', {},
        function(data){
            data = JSON.parse(data);
            //do task here
            const progress_bar_value = data['progress_bar'];
            const files = data['upload_files'];

            console.log(data);
            if(data['process'] !== 'Finished'){

                $('#progressBar').attr('aria-valuenow', progress_bar_value)
                    .css('width', progress_bar_value + '%').text(progress_bar_value + '%');

                for (let i = 0; i < files.length; i++){
                    let log = '<p>' + files[i] + '</p>';
                    if (files[i] !== '') logBox.append(log)
                }
                posts()
            }
            else {
                for (let i = 0; i < files.length; i++){
                    let log = '<p>' + files[i] + '</p>';
                    if (files[i] !== '') logBox.append(log)
                }
                if (data['upload_files'].length === 0){
                    $('#upload_files').text("There are not processed files.")
                }
            }
        }
    )
}
