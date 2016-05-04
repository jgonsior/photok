var photokApp = angular.module('photok', [
	'ngRoute',
	'photokControllers',
	'contestServices'
]);

photokApp.config(['$interpolateProvider', '$routeProvider', function($interpolateProvider, $routeProvider) {
	// avoid jinga / angular template conflict 
	// {{}} is for jinga
	// [[]] is for angular
	//$interpolateProvider.startSymbol('[[');
	//$interpolateProvider.endSymbol(']]');
	
	$routeProvider.when('/contests', {
		templateUrl: 'static/partials/contest-list.html',
		controller: 'ContestListController'
	}).
	when('/contests/:contestId', {
		templateUrl: 'static/partials/contest-detail.html',
		controller: 'ContestDetailController'
	}).
	otherwise({
		redirectTo: '/contests'
	})
}]);
