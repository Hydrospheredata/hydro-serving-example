
organization := "io.hydrosphere"
name := "robustrandomcut"
version := "0.1.0-SNAPSHOT"

scalaVersion := "2.11.12"

libraryDependencies ++= Dependencies.all

enablePlugins(JavaAppPackaging)
enablePlugins(DockerPlugin)
enablePlugins(AshScriptPlugin)


mainClass in Compile := Some("io.hydrosphere.rrcf.Main")
dockerBaseImage := "openjdk:jre-alpine"

packageName in Docker := packageName.value
