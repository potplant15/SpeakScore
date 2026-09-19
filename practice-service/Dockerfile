FROM maven:3.9-eclipse-temurin-21 AS build

WORKDIR /build

COPY pom.xml .
COPY src ./src

RUN mvn -B package -DskipTests

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /build/target/practice-service-0.1.0.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
