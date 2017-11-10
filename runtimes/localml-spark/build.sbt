lazy val sparkVersion = util.Properties.propOrElse("sparkVersion", "2.2.0")
lazy val sparkVersionLogger = taskKey[Unit]("Logs Spark version")

sparkVersionLogger := {
  val log = streams.value.log
  log.info(s"Spark version: $sparkVersion")
}

lazy val localSparkVersion = sparkVersion.substring(0,sparkVersion.lastIndexOf(".")).replace('.', '_')

name := s"spark-localml-serve-${localSparkVersion.replace('_', '.')}"
version := "1.0"
scalaVersion := "2.11.8"

lazy val sparkDependencies =
  Seq(
    "org.apache.spark" %% "spark-mllib" % sparkVersion,
    "io.hydrosphere" %% s"spark-ml-serving-$localSparkVersion" % "0.2.1"
  )

lazy val hdfsDependencies = {
  val hdfsV = "2.6.4"
  Seq(
    "org.apache.hadoop" % "hadoop-client" % hdfsV,
    "org.apache.hadoop" % "hadoop-hdfs" % hdfsV,
    "org.apache.hadoop" % "hadoop-common" % hdfsV
  )
}

lazy val akkaDependencies = {
  val akkaV = "2.4.14"
  val akkaHttpV = "10.0.0"
  Seq(
    "com.typesafe.akka" %% "akka-http-core" % akkaHttpV,
    "com.typesafe.akka" %% "akka-http" % akkaHttpV,
    "com.typesafe.akka" %% "akka-http-spray-json" % akkaHttpV,
    "com.typesafe.akka" %% "akka-http-jackson" % akkaHttpV,
    "com.typesafe.akka" %% "akka-http-xml" % akkaHttpV,
    "com.typesafe.akka" %% "akka-actor" % akkaV,
    "ch.megard" %% "akka-http-cors" % "0.1.10"
  )
}

resolvers ++= Seq(
  Resolver.sonatypeRepo("releases"),
  Resolver.sonatypeRepo("snapshots")
)

libraryDependencies ++= hdfsDependencies
libraryDependencies ++= akkaDependencies
libraryDependencies ++= sparkDependencies

mainClass in assembly := Some("io.hydrosphere.spark_runtime.Boot")

assemblyMergeStrategy in assembly := {
  case m if m.toLowerCase.endsWith("manifest.mf") => MergeStrategy.discard
  case PathList("META-INF", "services", "org.apache.hadoop.fs.FileSystem") => MergeStrategy.filterDistinctLines
  case m if m.startsWith("META-INF") => MergeStrategy.discard
  case PathList("javax", "servlet", xs@_*) => MergeStrategy.first
  case PathList("org", "apache", xs@_*) => MergeStrategy.first
  case PathList("org", "jboss", xs@_*) => MergeStrategy.first
  case "about.html" => MergeStrategy.rename
  case "reference.conf" => MergeStrategy.concat
  case PathList("org", "datanucleus", xs@_*) => MergeStrategy.discard
  case _ => MergeStrategy.first
}
test in assembly := {}

assembly := {assembly.dependsOn(sparkVersionLogger).value}
