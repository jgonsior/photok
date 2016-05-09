var photokControllers = angular.module('photokControllers', [
	'contestServices'
]);

photokControllers.controller('ContestListController', ['$scope', 'Contest',
function($scope, Contest) {
	$scope.contests = Contest.query();
	$scope.orderProp = 'createdDate';
}]);

photokControllers.controller('ContestDetailController', ['$scope', '$routeParams', 'Contest', 'ContestImages','ImageParticipation',
function($scope, $routeParams, Contest, ContestImages, ImageParticipation) {
	$scope.contest = Contest.get({contestId: $routeParams.contestId}, function(contest) {
	});
	$scope.images = ContestImages.get({contestId: $routeParams.contestId}, function(contest) {
	});

	// - - - Form for participation
	$scope.master = {};

	$scope.update = function(participation) {
		$scope.master = angular.copy(participation);
	};

	$scope.reset = function(form) {
		if (form) {
			form.$setPristine();
			form.$setUntouched();
		}
		$scope.participation = angular.copy($scope.master);
	};

	$scope.reset();
	// - - -

	$scope.sendImage = function () {

		alert("SENDING: "+$scope.participation.title);

    // call login from service
    ImageParticipation.sendImage($scope.participation.title,"exif-fake-data","1","1")
      // handle success
      .then(function () {
				alert('It worked!');
      })
      // handle error
      .catch(function () {
        //$scope.error = true;
        alert('An error occurred');
      });

			alert("SENDING: Done");

  };

}]);

photokControllers.controller('CreateContestController', ['$scope', '$routeParams', 'Contest', 'ContestImages',
function($scope, $routeParams, Contest, ContestImages) {
	$scope.master = {};

  $scope.update = function(contest) {
    $scope.master = angular.copy(contest);
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
