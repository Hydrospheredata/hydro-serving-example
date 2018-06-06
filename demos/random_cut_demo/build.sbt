import Dependencies._

lazy val root = (project in file(".")).
  settings(
    inThisBuild(List(
      organization := "com.example",
      scalaVersion := "2.11.12",
      version := "0.1.0-SNAPSHOT"
    )),
    name := "robustrandomcut",
    libraryDependencies += scalaTest % Test
  )

libraryDependencies ++= Seq(
  "com.typesafe.akka" %% "akka-actor" % "2.5.12",
  "com.typesafe.akka" %% "akka-testkit" % "2.5.12" % Test,
  "io.hydrosphere" %% "serving-grpc-scala" % "0.1.6"
)

libraryDependencies ++= Seq(
  "io.circe" %% "circe-core",
  "io.circe" %% "circe-generic",
  "io.circe" %% "circe-parser"
).map(_ % "0.9.3")

enablePlugins(JavaAppPackaging)
enablePlugins(DockerPlugin)
enablePlugins(AshScriptPlugin)


mainClass in Compile := Some("example.Main")
dockerBaseImage := "openjdk:jre-alpine"

packageName in Docker := packageName.value
dockerExposedPorts := Seq(9080)