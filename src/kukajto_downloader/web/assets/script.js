const analyze = document.querySelector(".submit-btn");
const download_video = document.querySelector(".download-video-btn");
const download_subs = document.querySelector(".download-subs-btn");
const player = document.querySelector(".player");

const video_result = document.querySelector(".video-result");
const subs_result = document.querySelector(".subs-result");

const analyze_msg = ["Analyze", "Analyzing ..."];
const download_video_msg = ["Download video", "Downloading video ..."];
const download_subs_msg = ["Download subs", "Downloading subs ..."];

const printError = (error) => {
    alert("Error! " + error.errorText);
    console.error(error.errorTraceback);
}

eel.expose(updateAnalyzeBar);
function updateAnalyzeBar(percent) {
    analyze.style.setProperty("--percent", percent + "%");
}

eel.expose(updateVideoDownloadBar);
function updateVideoDownloadBar(percent) {
    download_video.style.setProperty("--percent", percent + "%");
}

eel.expose(updateSubsDownloadBar);
function updateSubsDownloadBar(percent) {
    download_subs.style.setProperty("--percent", percent + "%");
}

const changeAnalyzeButtonState = (state) => {
    analyze.disabled = state;
}

const changeDownloadButtonState = (state) => {
    download_video.disabled = state;
    download_subs.disabled = state;
}

analyze.addEventListener("click", () => {
    analyze.innerHTML = analyze_msg[1];
    changeAnalyzeButtonState(true);
    updateAnalyzeBar(20);

    try {
        eel.analyze()().then((data)=>{
            let video = data[0];
            let subs = data[1];
    
            console.log(video);
            console.log(subs);
            
            player.src = video;
            
            if (video.length > 0) {
                download_video.disabled = false;
                updateVideoDownloadBar(100);
                video_result.innerHTML = video;
                video_result.href = video;
            }
            if (subs.length > 0) {
                download_subs.disabled = false;
                updateSubsDownloadBar(100);
                subs_result.innerHTML = subs;
                subs_result.href = subs;
            }
        }).catch((error)=> {
            printError(error);
        }).finally(() => {        
            analyze.innerHTML = analyze_msg[0];
            changeAnalyzeButtonState(false);
            updateAnalyzeBar(100);
        });
    } catch (error) {
        console.error(error);
        analyze.innerHTML = analyze_msg[0];
        changeAnalyzeButtonState(false);
        updateAnalyzeBar(100);
    }
});

download_video.addEventListener("click", () => {
    const changeButtonsState = (state) => {
        changeAnalyzeButtonState(state);
        changeDownloadButtonState(state);
        download_video.innerHTML = download_video_msg[state ? 1 : 0];
    }

    changeButtonsState(true);

    try {
        eel.download_video().then((data) => {
            if (!data) {
                alert("Failed to download video.");
            }
        }).catch((error)=>{
            printError(error);
        }).finally(()=>{
            changeButtonsState(false);
        });
    } catch (error) {
        console.error(error);
        changeButtonsState(false);
    }
});

download_subs.addEventListener("click", () => {
    const changeButtonsState = (state) => {
        changeAnalyzeButtonState(state);
        changeDownloadButtonState(state)
        download_subs.innerHTML = download_subs_msg[state ? 1 : 0];
    }

    changeButtonsState(true);

    try {
        eel.download_subs().then((data) => {
            if (!data) {
                alert("Failed to download subs.");
            }
        }).catch((error)=>{
            printError(error);
        }).finally(()=>{
            changeButtonsState(false)
        });
    } catch (error) {
        console.error(error);
        changeButtonsState(false);
    }
});

// https://serial.kukaj.io/the-last-of-us/S01E06?source=1&subs=2&lng=EN

// https://s-delivery44.mxdcontent.net/v/4da8a368a33491d37fb386fb6907059b.mp4?s=uKWv4j5i4sQsWLtTQm64lw&e=1677265958&_t=1677250498
// https://kukaj.io/subtitles/v2/63f2defa4b763.vtt
