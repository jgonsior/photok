'use strict';

var photokApp = angular.module('photok', [
	'ngRoute',
	'photokControllers',
	'contestServices'
]);

photokApp.config(['$locationProvider', '$routeProvider', function($locationProvider, $routeProvider) {
	// avoid jinga / angular template conflict
	// {{}} is for jinga
	// [[]] is for angular
	//$interpolateProvider.startSymbol('[[');
	//$interpolateProvider.endSymbol(']]');

	$routeProvider.when('/', {
		templateUrl: 'static/partials/homepage.html'
	}).
	when('/admin', {
		templateUrl: 'static/partials/adminpage.html'
	}).
	when('/add', {
		templateUrl: 'static/partials/create-contest.html'
	}).
	when('/contests', {
		templateUrl: 'static/partials/contest-list.html',
		controller: 'ContestListController'
	}).
	when('/contests/:contestId', {
		templateUrl: 'static/partials/contest-detail.html',
		controller: 'ContestDetailController'
	}).
	when('/user/login', {
		templateUrl: 'static/partials/homepage.html',
	}).
	otherwise({
		templateUrl: 'static/partials/error-404.html'
	});

	$locationProvider.html5Mode(true);
}]);
