import sbt._

object Dependencies {
  lazy val scalaTest = Seq("org.scalatest" %% "scalatest" % "3.0.5")

  lazy val akka = Seq(
    "com.typesafe.akka" %% "akka-actor" % "2.5.12",
    "com.typesafe.akka" %% "akka-testkit" % "2.5.12" % Test
  )

  lazy val grpc = Seq(
    "io.hydrosphere" %% "serving-grpc-scala" % "0.1.6"
  )

  lazy val circe = Seq(
    "io.circe" %% "circe-core",
    "io.circe" %% "circe-generic",
    "io.circe" %% "circe-parser"
  ).map(_ % "0.9.3")

  lazy val all = scalaTest ++ akka ++ grpc ++ circe
}
