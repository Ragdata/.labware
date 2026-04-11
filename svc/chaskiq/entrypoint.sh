#!/bin/sh
set -e
rm -f /usr/src/app/tmp/pids/server.pid
exec "$@"
echo "Running database migrations..."
bundle exec rails db:setup || true
bundle exec rails db:migrate
echo "Finished running database migrations."
echo "Running packages update..."
bundle exec rails packages:update
echo "Finished packages update."
if [ ! -f /usr/src/app/admin_generated ]; then
		echo "/usr/src/app/admin_generated not found, executing admin generation.."
		bundle exec rake admin_generator
		touch /usr/src/app/admin_generated
		echo "Admin generation finished !"
fi
bundle exec rails s -b 0.0.0.0 -p 3000
