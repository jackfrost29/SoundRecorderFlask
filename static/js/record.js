let audio_in = { audio: true };
let blob = null;

navigator.mediaDevices.getUserMedia(audio_in).then(function (mediaStreamObj) {

    const record = document.getElementById("record-button");
    const _stop = document.getElementById("stop-button");
    const submit = document.getElementById("submit-button");
    const edit = document.getElementById("edit-button");

    const mediaRecorder = new MediaRecorder(mediaStreamObj);

    let chunks = [];

    record.onclick = function () {
        record.disabled = true;
        _stop.disabled = false;
        submit.disabled = true;
        edit.disabled = true;
        document.getElementById('delete-button').disabled = true;

        mediaRecorder.start();
    }
    _stop.onclick = function () {
        _stop.disabled = true;
        record.disabled = false;
        submit.disabled = false;
        edit.disabled = false;
        document.getElementById('delete-button').disabled = false;

        mediaRecorder.stop();
    }
    mediaRecorder.ondataavailable = function (e) {
        chunks.push(e.data)
    }

    mediaRecorder.onstop = function (e) {
        blob = new Blob(chunks, { 'type': 'audio/webm;' });
        document.getElementById("audio-tag").src = window.URL.createObjectURL(blob);

        chunks = [];
    }

}).catch(function (error) {
    console.log(error.name, error.message);
});

async function delete_request(){
    const formData = new FormData();
    formData.append("delete", "true");
    formData.append("sentence_id", document.getElementById("bangla-sentence").getAttribute("_id"));
    formData.append("sentence_text", document.getElementById("bangla-sentence").innerHTML);

    try {
        const response = await fetch(window.location.href, {
            method: "POST",
            body: formData,
            mode: "cors",
        });
        if (response.status === 200) window.location.reload();
    } catch (e) {
        console.log(e);
    }
}

async function submit_request(){
    const formData = new FormData();
    formData.append("sentence_id", document.getElementById("bangla-sentence").getAttribute("_id"));
    formData.append("sentence_text", document.getElementById("bangla-sentence").innerHTML);
    formData.append("recorded_audio", blob, "temp");

    try {
        const response = await fetch(window.location.href, {
            method: "POST",
            body: formData,
            mode: "cors",
        });
        if (response.status === 200) window.location.reload();
    } catch (e) {
        console.log(e);
    }
}



function edit_function() {
    sentence = prompt("Modify the sentence on the box.", document.getElementById("bangla-sentence").innerHTML);
    if (sentence) {
        document.getElementById("bangla-sentence").innerHTML = sentence;
    }

}

function delete_function() {
    let _delete = window.confirm("Are you sure you want to delete the sentence?");
    if (_delete) {
        delete_request();
    }
}

function submit_function() {
    // only submit the audio when it has been recorded.
    // also has to mention if the text was edited. 
    // whether the text was edited can be found from the property of the text.


    // check if the audio is being recorded.

    submit_request();
}

function show_not_recorded_error() {
    error_element = document.getElementById("not-recorder-error");
    error_element.innerHTML = "Please Record the audio first!"

    if (error_element.style.color == "blue") { error_element.style.color = "red"; }
    else if (error_element.style.color == "red") { error_element.style.color = "green"; }
    else { error_element.style.color = "blue"; }

}
