/* Declare Variables */
var minutes = document.getElementById("minutes");
var seconds = document.getElementById("seconds");
var on_off = document.getElementsByClassName("start_pause");
var time_left = parseInt(document.getElementById("user_time").innerHTML, 10) * 60;
var timer_clock;


function countdown() {
	let str1 = "start";
	let str2 = "pause";
	if (on_off[0].id === str1)
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
	
	if (seconds_value < 10)
		seconds_value = '0' + seconds_value;
	minutes.innerHTML = minutes_value;
	seconds.innerHTML = seconds_value;
	if (time_left == 0)
	{
		clearInterval(timer_clock);
	}
	else
	{
		time_left = time_left - 1;
	}
}

function add_time(value) {
	clearInterval(timer_clock);
	time_left = time_left + (value * 60);
	timer_clock = setInterval(inCountdown, 1000);
}

function finish() {
	clearInterval(timer_clock);
}
