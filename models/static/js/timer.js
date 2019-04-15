/* Declare Variables */
var minutes = document.getElementById("minutes");
var seconds = document.getElementById("seconds");
var on_off = document.getElementsByClassName("start_pause");
var user_time = document.getElementById("user_time")
var progress_bar = document.getElementById("progress-bar");
var time_left = parseInt(user_time.innerHTML, 10) * 60;
var timer_clock;
var original_time = time_left;

function countdown() {
	if (on_off[0].id === "start")
	{
		document.getElementById("start").innerHTML = 'Pause';
		document.getElementById("start").id = "pause";
		timer_clock = setInterval(inCountdown, 1000);
	}
	else
	{
		document.getElementById("pause").innerHTML = 'Begin';
		document.getElementById("pause").id = "start";
		clearInterval(timer_clock);
	}	
}

function inCountdown() {
	let minutes_value = Math.floor((time_left / 60));
	let seconds_value = Math.floor((time_left % 60));
	let percentage = (1 - time_left / original_time) * 100;

	console.log(percentage);
	if (seconds_value < 10)
		seconds_value = '0' + seconds_value;
	user_time.innerHTML = minutes_value;
	seconds.innerHTML = seconds_value;
	progress_bar.style.width = percentage.toString().concat('%');
	if (time_left == 0)
	{
		clearInterval(timer_clock);
		playAudio();
	}
	else
	{
		time_left = time_left - 1;
	}
}

function add_time(value) {
	if (on_off[0].id === "start")
	{
		time_left = time_left + (value * 60);
		user_time.innerHTML = time_left / 60;
	}
	else
	{
		clearInterval(timer_clock);
		time_left = time_left + (value * 60);
		timer_clock = setInterval(inCountdown, 1000);
	}
}

function finish() {
	console.log('in finish function javascript');
	clearInterval(timer_clock);
}

function playAudio() {
	var audio = document.getElementById("alarm-audio");
	audio.loop = false;
	audio.play();
}
