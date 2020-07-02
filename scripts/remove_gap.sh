window_gap=$(bspc config window_gap)
window_gap=$(($window_gap - 10))
bspc config window_gap $window_gap
