var contestServices = angular.module('contestServices', ['ngResource']);

contestServices.factory('Contest', ['$resource',
												 function($resource){
													 return $resource('api/contests/:contestId', {}, {
														 query: {method:'GET', params:{contestId:'contests'}, isArray:true}
													 });
												 }]);
