var photokControllers = angular.module('photokControllers', []);

photokControllers.controller('ContestListController', ['$scope', 'Contest',
														 function($scope, Contest) {
															 $scope.contests = Contest.query();
														 }]);

photokControllers.controller('ContestDetailController', ['$scope', '$routeParams', 'Contest',
														 function($scope, $routeParams, Contest) {
															 $scope.contest = Contest.get({contestId: $routeParams.contestId}, function(contest) {
															 });
														 }]);
