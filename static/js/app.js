'use strict';

var photokApp = angular.module('photok', [
	'ngRoute',
	'photokServices',
	'photokControllers'
]);

photokApp.config(['$locationProvider', '$routeProvider', function($locationProvider, $routeProvider) {

	$routeProvider.when('/', {
		title: 'Home',
		templateUrl: 'static/partials/homepage.html'
	}).
	when('/admin', {
		title: 'Admin',
		templateUrl: 'static/partials/adminpage.html'
	}).
	when('/add', {
		title: 'Add contest',
		templateUrl: 'static/partials/create-contest.html',
		controller: 'CreateContestController'
	}).
	when('/contests', {
		title: 'Contests',
		templateUrl: 'static/partials/contest-list.html',
		controller: 'ContestListController'
	}).
	when('/contests/:contestId', {
		title: 'Contest',
		templateUrl: 'static/partials/contest-detail.html',
		controller: 'ContestDetailController'
	}).
	when('/user/login', {
		title: 'Log in',
		templateUrl: 'static/partials/homepage.html',
	}).
	otherwise({
		title: 'Oops',
		templateUrl: 'static/partials/error-404.html'
	});

	$locationProvider.html5Mode(true);
}]);

// In order to change the <title> tag depending on the page
photokApp.run(['$rootScope', function($rootScope) {
    $rootScope.$on('$routeChangeSuccess', function (event, current, previous) {
        $rootScope.title = current.$$route.title;
    });
}]);
