package io.hydrosphere.spark_runtime

import org.apache.spark.ml.{PipelineModel, Transformer}
import org.apache.spark.ml.param.Param

object SparkUtils {
  private[this] val INPUTCOLS = Array("inputCol", "featuresCol")
  private[this] val OUTPUTCOLS = Array("outputCol", "predictionCol", "probabilityCol", "rawPredictionCol")
  private[this] val LABELCOLS = Array("labelCol")

  implicit class PumpedPipelineModel(val pipelineModel: PipelineModel) {
    private[this] val inParams = extract(INPUTCOLS)
    private[this] val outParams = extract(OUTPUTCOLS)
    private[this] val labelParams = extract(LABELCOLS)

    private def extract(params: Seq[String], transformer: Transformer): Seq[String] = {
      params.map{ i =>
          if (transformer.hasParam(i)) {
            val param = transformer.getParam(i).asInstanceOf[Param[String]]
            Some(transformer.get(param).get)
          } else {
            None
          }
      }.filter(_.isDefined).map(_.get)
    }

    private def extract(params: Seq[String]): Seq[String] = {
      pipelineModel.stages.flatMap(extract(params, _))
    }

    def inputCols = {
      if (labelParams.isEmpty) {
        inParams.diff(outParams).toList
      } else {
        val trains = pipelineModel.stages.filter { stage =>
          val outs = extract(OUTPUTCOLS, stage)
          val flag = outs.containsSlice(labelParams)
          flag
        }.flatMap(extract(INPUTCOLS, _))

        inParams.diff(outParams).diff(trains)
      }
    }

    def outputCols = {
      outParams.diff(inParams)
    }
  }
}
