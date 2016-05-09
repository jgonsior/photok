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

photokControllers.controller('CreateContestController', ['$scope', '$routeParams', 'Contest', 'ContestImages',
function($scope, $routeParams, Contest, ContestImages) {
	$scope.master = {};

  $scope.update = function(user) {
    $scope.master = angular.copy(user);
  };

  $scope.reset = function(form) {
    if (form) {
      form.$setPristine();
      form.$setUntouched();
    }
    $scope.contest = angular.copy($scope.master);
  };

  $scope.reset();
}]);
