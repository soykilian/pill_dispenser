var describeArc, polarToCartesian, setCaptions;

polarToCartesian = function(centerX, centerY, radius, angleInDegrees) {
  var angleInRadians;
  angleInRadians = (angleInDegrees - 90) * Math.PI / 180.0;
  return {
    x: centerX + radius * Math.cos(angleInRadians),
    y: centerY + radius * Math.sin(angleInRadians)
  };
};

describeArc = function(x, y, radius, startAngle, endAngle) {
  var arcSweep, end, start;
  start = polarToCartesian(x, y, radius, endAngle);
  end = polarToCartesian(x, y, radius, startAngle);
  arcSweep = endAngle - startAngle <= 180 ? '0' : '1';
  return ['M', start.x, start.y, 'A', radius, radius, 0, arcSweep, 0, end.x, end.y].join(' ');
};

setCaptions = function() {
  var dot, hour, hourArc, minArc, minute, now, pos;
  now = new Date();
  hour = now.getHours() % 12;
  minute = now.getMinutes();
  hourArc = (hour * 60 + minute) / (12 * 60) * 360;
  minArc = minute / 60 * 360;
  $('.clockArc.hour').attr('d', describeArc(500, 240, 150, 0, hourArc));
  $('.clockArc.minute').attr('d', describeArc(500, 240, 170, 0, minArc));
  $('.clockDot.hour').attr('d', describeArc(500, 240, 150, hourArc - 3, hourArc));
  $('.clockDot.minute').attr('d', describeArc(500, 240, 170, minArc - 1, minArc));
  dot = $(".clockDot.hour");
  pos = polarToCartesian(500, 240, 150, hourArc);
  dot.attr("cx", pos.x);
  dot.attr("cy", pos.y);
  dot = $(".clockDot.minute");
  pos = polarToCartesian(500, 240, 170, minArc);
  dot.attr("cx", pos.x);
  dot.attr("cy", pos.y);
  return $('#time').text(moment().format('H:mm'));
};


runClock = function()
{
$('#day').text(moment().format('dddd'));

$('#date').text(moment().format('MMMM D'));

setCaptions();

setInterval(function() {
  return setCaptions();
}, 10 * 1000);

$(function() {
  TweenMax.staggerFrom(".clockArc", .5, {
    drawSVG: 0,
    ease: Power3.easeOut
  }, 0.3);
  TweenMax.from("#time", 1.0, {
    attr: {
      y: 350
    },
    opacity: 0,
    ease: Power3.easeOut,
    delay: 0.5
  });
  TweenMax.from(".dayText", 1.0, {
    attr: {
      y: 310
    },
    opacity: 0,
    delay: 1.0,
    ease: Power3.easeOut
  });
  return TweenMax.from(".dateText", 1.0, {
    attr: {
      y: 350
    },
    opacity: 0,
    delay: 1.5,
    ease: Power3.easeOut
  });
});
}