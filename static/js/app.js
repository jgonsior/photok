'use strict';

var photokApp = angular.module('photok', [
	'ui.router',
	'photokServices',
	'photokControllers',
	'ngStorage'
]);

photokApp.factory('httpRequestInterceptor', ['$localStorage', function ($localStorage) {
  return {
    request: function (config) {

      config.headers['Authorization'] = 'JWT ' + $localStorage.currentUser.access_token;
      return config;
    }
  };
}]);

photokApp.config(['$locationProvider', '$stateProvider', '$urlRouterProvider', '$httpProvider', function($locationProvider, $stateProvider, $urlRouterProvider, $httpProvider) {

	$httpProvider.interceptors.push('httpRequestInterceptor');
	//for any unmatched url redirect to /
	$urlRouterProvider.otherwise("/error-404");

	$stateProvider
		.state('contest-list', {
			url: "/contests",
			title: "Contest List",
			templateUrl: "static/partials/contest-list.html",
			controller: 'ContestListController'
		})
		.state('create-contest', {
			url: "/add",
			title: "Create new Contest",
			templateUrl: "static/partials/create-contest.html",
			controller: "CreateContestController"
		})
		.state('edit-contest', {
			url: "/edit/:contestId",
			title: "Edit contest",
			templateUrl: 'static/partials/edit-contest.html',
			controller: "EditContestController"
		})
		.state('contest-detail', {
			url: "/contests/:contestId",
			title: "View Contest",
			templateUrl: "static/partials/contest-detail.html",
			controller: "ContestDetailController"
		})
		.state('vote', {
			url: "/vote/:contestId",
			title: 'Vote for contest',
			templateUrl: 'static/partials/vote-contest.html',
			controller: 'VoteContestController'
		})
		.state('error-404', {
			url: "error-404",
			title: "Oops",
			templateUrl: "static/partials/error-404.html"
		});

		// make urls look nicer -> without the annoying #
		$locationProvider.html5Mode(true);
}]);

// In order to change the <title> tag depending on the page
photokApp.run(['$rootScope', '$state',  function($rootScope, $state) {
	$rootScope.$on('$stateChangeSuccess', function (event, current, previous) {
		$rootScope.title = $state.current.title;
	});
}]);

