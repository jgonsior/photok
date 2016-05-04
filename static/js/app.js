var photokApp = angular.module('photok', [
	'ngRoute',
	'phonecatControllers',
	'phonecatServices'
]);

photokApp.config(['$interpolateProvider', '$routeProvider', function($interpolateProvider, $routeProvider) {
	// avoid jinga / angular template conflict 
	// {{}} is for jinga
	// [[]] is for angular
	$interpolateProvider.startSymbol('[[');
	$interpolateProvider.endSymbol(']]');
	
	$routeProvider.when('/contests', {
		templateUrl: 'partials/contest-list.html',
		controller: 'ContestListController'
	}).
	when('/contests/:contestId', {
		templateUrl: 'partials/contest-detail.html',
		controller: 'ContestDetailController'
	}).
	otherwise({
		redirectTo: '/contests'
	})
}]);
