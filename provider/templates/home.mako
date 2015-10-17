<%inherit file='base.mako' />

% if user:
<p>You are logged in as: ${ user }</p>
<p><a href="${ request.route_url('logout') }">Logout</a></p>
% else:
<p>You are not logged in!</p>
<p><a href="${ request.route_url('login') }">Login</a></p>
% endif
