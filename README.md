### Steps for launch

1. Run services
> docker-compose up -d
2. Create superuser 
> docker exec -it csvGenerator python manage.py createsuperuser
3. Write username, email and password
4. [Open in browser schemas](http://localhost:8080/)
5. [Open in browser admin panel](http://localhost:8080/admin)