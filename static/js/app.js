'use strict';

var photokApp = angular.module('photok', [
	'ngRoute',
	'contestServices',
	'photokControllers'
]);

photokApp.config(['$locationProvider', '$routeProvider', function($locationProvider, $routeProvider) {
	// avoid jinga / angular template conflict
	// {{}} is for jinga
	// [[]] is for angular
	//$interpolateProvider.startSymbol('[[');
	//$interpolateProvider.endSymbol(']]');

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
		templateUrl: 'static/partials/create-contest.html'
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

photokApp.run(['$rootScope', function($rootScope) {
    $rootScope.$on('$routeChangeSuccess', function (event, current, previous) {
        $rootScope.title = current.$$route.title;
    });
}]);
