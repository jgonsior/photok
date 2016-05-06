var contestServices = angular.module('contestServices', ['ngResource']);

contestServices.factory('Contest', ['$resource',
function($resource){
	return $resource('api/contests/:contestId', {}, {
		query: {method:'GET', params:{contestId:''}, isArray:true}
	});
}]);

contestServices.factory('ContestImages', ['$resource',
function($resource){
	return $resource('api/images/contest/:contestId', {}, {
		query: {method:'GET', params:{contestId:''}, isArray:true}
	});
}]);
