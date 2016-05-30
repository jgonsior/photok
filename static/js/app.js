'use strict';

var photokApp = angular.module('photok', [
	'ui.router',
	'photokServices',
	'photokControllers',
	'ngStorage',
	'ngFileUpload'
]);

photokApp.factory('httpRequestInterceptor', ['$localStorage', '$injector', function ($localStorage, $injector) {
	return {
		request: function (config) {

			if($localStorage.currentUser) {
				//yay, we're logged in!
				config.headers['Authorization'] = 'JWT ' + $localStorage.currentUser.access_token;
			}
			return config;
		}
	};
}]);

photokApp.config(['$locationProvider', '$stateProvider', '$urlRouterProvider', '$httpProvider', function($locationProvider, $stateProvider, $urlRouterProvider, $httpProvider) {

	$httpProvider.interceptors.push('httpRequestInterceptor');

	//for any unmatched url redirect to an error page
	$urlRouterProvider.otherwise("contests");

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
		.state('login', {
			url: "/login?from",
			params: {
				from: "contest-list"
			},
			title: "Please log yourself in",
			templateUrl: 'static/partials/login.html',
			controller: 'LoginController'
		})
		.state('logout', {
			url: "/logout",
			title: "logging you out…",
			templateUrl: 'static/partials/logout.html',
			controller: 'LogoutController'
		})
		.state('error-404', {
			url: "/error-404",
			title: "Oops",
			templateUrl: "static/partials/error-404.html"
		});


	// make urls look nicer -> without the annoying #
		$locationProvider.html5Mode(true);
}]);

// In order to change the <title> tag depending on the page
photokApp.run(['$rootScope', '$state', '$localStorage', function($rootScope, $state, $localStorage) {
	$rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams, options) {
		if(!$localStorage.currentUser) {
			if(toState.name !== "login") {
				//stop the default route
				event.preventDefault();
				//redirect to login page
				$state.go('login', {from: toState.name});
			}
		}
	});

	$rootScope.$on('$stateChangeSuccess', function (event, current, previous) {
		$rootScope.title = $state.current.title;
	});
}]);
