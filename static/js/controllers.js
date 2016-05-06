var photokControllers = angular.module('photokControllers', []);

photokControllers.controller('ContestListController', ['$scope', 'Contest',
function($scope, Contest) {
	$scope.contests = Contest.query();
	$scope.orderProp = 'createdDate';
}]);

photokControllers.controller('ContestDetailController', ['$scope', '$routeParams', 'Contest', 'ContestImages',
function($scope, $routeParams, Contest, ContestImages) {
	$scope.contest = Contest.get({contestId: $routeParams.contestId}, function(contest) {
	});
	$scope.images = ContestImages.get({contestId: $routeParams.contestId}, function(contest) {
	});
}]);
