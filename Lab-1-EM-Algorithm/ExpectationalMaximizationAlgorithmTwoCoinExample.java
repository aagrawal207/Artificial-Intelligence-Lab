public class ExpectationalMaximizationAlgorithmTwoCoinExample {
    private final static int TOTAL_TRIALS = 10000;
    private final static double ACTUAL_PROBABILITY_TO_CHOOSE_COIN_1 = 0.7;
    private final static double ACTUAL_PROBABILITY_THAT_COIN_1_HAVE_HEAD = 0.6;
    private final static double ACTUAL_PROBABILITY_THAT_COIN_2_HAVE_HEAD = 0.3;
    private static double estimatedProbabilityToChooseCoin1;
    private static double estimatedProbabilityThatCoin1HaveHead;
    private static double estimatedProbabilityThatCoin2HaveHead;
    private static int[] trailResultObserved = new int[TOTAL_TRIALS];
    private static int totalHeads = 0;

    public static void main(String[] args) {
        System.out.println("Test value of p: " + ACTUAL_PROBABILITY_TO_CHOOSE_COIN_1);
        System.out.println("Test value of p1: " + ACTUAL_PROBABILITY_THAT_COIN_1_HAVE_HEAD);
        System.out.println("Test value of p2: " + ACTUAL_PROBABILITY_THAT_COIN_2_HAVE_HEAD);
        for (int i = 0; i < TOTAL_TRIALS; i++) {
            if (Math.random() < ACTUAL_PROBABILITY_TO_CHOOSE_COIN_1) {
                if (Math.random() < ACTUAL_PROBABILITY_THAT_COIN_1_HAVE_HEAD) {
                    trailResultObserved[i] = 1;
                    totalHeads++;
                } else {
                    trailResultObserved[i] = 0;
                }
            } else {
                if (Math.random() < ACTUAL_PROBABILITY_THAT_COIN_2_HAVE_HEAD) {
                    trailResultObserved[i] = 1;
                    totalHeads++;
                } else {
                    trailResultObserved[i] = 0;
                }
            }
        }
        System.out.println("Total heads: " + totalHeads + " out of " + TOTAL_TRIALS);
        estimateNewProbabilities();
        System.out.println("Final value of p: " + estimatedProbabilityToChooseCoin1);
        System.out.println("Final value of p1: " + estimatedProbabilityThatCoin1HaveHead);
        System.out.println("Final value of p2: " + estimatedProbabilityThatCoin2HaveHead);
    }

    private static void estimateNewProbabilities() {
        int totalIterations = 0;
        double e = 0.0000000000000000001;
        double initialProbabilityToChooseCoin1 = Math.random();
        double initialProbabilityThatCoin1HaveHead = Math.random();
        double initialProbabilityThatCoin2HaveHead = Math.random();
        System.out.println("Initial value of p: " + initialProbabilityToChooseCoin1);
        System.out.println("Initial value of p1: " + initialProbabilityThatCoin1HaveHead);
        System.out.println("Initial value of p2: " + initialProbabilityThatCoin2HaveHead);
        double updatedProbabilityToChooseCoin1 = initialProbabilityToChooseCoin1;
        double updatedProbabilityThatCoin1HaveHead = initialProbabilityThatCoin1HaveHead;
        double updatedProbabilityThatCoin2HaveHead = initialProbabilityThatCoin2HaveHead;
        do {
            totalIterations++;
            double sumHiddenVariableZExpectation = 0;
            double sumHiddenVariableZExpectationTimesObservedVariable = 0;
            estimatedProbabilityToChooseCoin1 = updatedProbabilityToChooseCoin1;
            estimatedProbabilityThatCoin1HaveHead = updatedProbabilityThatCoin1HaveHead;
            estimatedProbabilityThatCoin2HaveHead = updatedProbabilityThatCoin2HaveHead;
            for (int j = 0; j < TOTAL_TRIALS; j++) {
                int observedVariable = trailResultObserved[j];
                // E-step
                double probabilityThatHeadFromCoin1 = (estimatedProbabilityToChooseCoin1
                        * Math.pow(estimatedProbabilityThatCoin1HaveHead, observedVariable)
                        * Math.pow(1 - estimatedProbabilityThatCoin1HaveHead, 1 - observedVariable));
                double probabilityThatHeadFromCoin2 = ((1 - estimatedProbabilityToChooseCoin1)
                        * Math.pow(estimatedProbabilityThatCoin2HaveHead, observedVariable)
                        * Math.pow(1 - estimatedProbabilityThatCoin2HaveHead, 1 - observedVariable));
                double hiddenVariableZExpectation = probabilityThatHeadFromCoin1
                        / (probabilityThatHeadFromCoin1 + probabilityThatHeadFromCoin2);
                sumHiddenVariableZExpectation += hiddenVariableZExpectation;
                sumHiddenVariableZExpectationTimesObservedVariable += observedVariable * hiddenVariableZExpectation;
            }
            // M-step
            updatedProbabilityToChooseCoin1 = sumHiddenVariableZExpectation / TOTAL_TRIALS;
            updatedProbabilityThatCoin1HaveHead = sumHiddenVariableZExpectationTimesObservedVariable
                    / sumHiddenVariableZExpectation;
            updatedProbabilityThatCoin2HaveHead = (totalHeads - sumHiddenVariableZExpectationTimesObservedVariable)
                    / (TOTAL_TRIALS - sumHiddenVariableZExpectation);
        } while (totalIterations < 10000);
        System.out.println("Total iteration: " + totalIterations);

    }
}
