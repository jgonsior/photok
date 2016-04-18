var photokApp = angular.module('photok', []);

photokApp.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
}]);

photokApp.controller('homepage', function ($scope) {
  $scope.message = "message-for-homepage";
  console.log($scope.message);
});

photokApp.controller('test', function ($scope) {
  $scope.message = "message-for-others";
});
