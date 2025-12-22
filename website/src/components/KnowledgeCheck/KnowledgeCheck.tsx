import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

interface KnowledgeCheckOption {
  id: string;
  text: string;
  isCorrect: boolean;
}

interface KnowledgeCheckProps {
  question: string;
  options: KnowledgeCheckOption[];
  explanation?: string;
  className?: string;
  onComplete?: (result: { selected: string | null; correct: boolean; score: number }) => void;
}

const KnowledgeCheck: React.FC<KnowledgeCheckProps> = ({
  question,
  options,
  explanation,
  className,
  onComplete
}) => {
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [showExplanation, setShowExplanation] = useState(false);

  // Handle option selection
  const handleOptionSelect = (optionId: string) => {
    if (!isSubmitted) {
      setSelectedOption(optionId);
    }
  };

  // Submit the answer
  const handleSubmit = () => {
    if (selectedOption && !isSubmitted) {
      const correct = options.find(opt => opt.id === selectedOption)?.isCorrect || false;
      setIsCorrect(correct);
      setIsSubmitted(true);
      setShowExplanation(true);

      if (onComplete) {
        onComplete({
          selected: selectedOption,
          correct,
          score: correct ? 1 : 0
        });
      }
    }
  };

  // Reset the check
  const handleReset = () => {
    setSelectedOption(null);
    setIsSubmitted(false);
    setIsCorrect(false);
    setShowExplanation(false);
  };

  // Calculate score
  const score = isCorrect ? 1 : 0;

  return (
    <div
      className={clsx(
        styles.knowledgeCheck,
        { [styles.submitted]: isSubmitted },
        { [styles.correct]: isSubmitted && isCorrect },
        { [styles.incorrect]: isSubmitted && !isCorrect },
        className
      )}
      role="region"
      aria-label="Knowledge check"
    >
      <div className={styles.questionContainer}>
        <h4 className={styles.question}>{question}</h4>

        <div className={styles.optionsContainer}>
          {options.map((option, index) => (
            <label
              key={option.id}
              className={clsx(
                styles.optionLabel,
                { [styles.selected]: selectedOption === option.id },
                { [styles.correct]: isSubmitted && option.isCorrect },
                { [styles.incorrect]: isSubmitted && !option.isCorrect && selectedOption === option.id },
                { [styles.disabled]: isSubmitted }
              )}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault();
                  handleOptionSelect(option.id);
                } else if (e.key === 'ArrowDown' && index < options.length - 1) {
                  // Move focus to next option
                  const nextOption = document.getElementById(`option-${options[index + 1].id}`);
                  nextOption?.focus();
                } else if (e.key === 'ArrowUp' && index > 0) {
                  // Move focus to previous option
                  const prevOption = document.getElementById(`option-${options[index - 1].id}`);
                  prevOption?.focus();
                }
              }}
              tabIndex={isSubmitted ? -1 : 0}
            >
              <input
                type="radio"
                name="knowledge-check-options"
                id={`option-${option.id}`}
                value={option.id}
                checked={selectedOption === option.id}
                onChange={() => handleOptionSelect(option.id)}
                disabled={isSubmitted}
                className={styles.optionInput}
              />
              <span className={styles.optionText}>{option.text}</span>
              {isSubmitted && option.isCorrect && (
                <span className={styles.correctIndicator} aria-label="Correct answer">✓</span>
              )}
              {isSubmitted && !option.isCorrect && selectedOption === option.id && (
                <span className={styles.incorrectIndicator} aria-label="Incorrect answer">✗</span>
              )}
            </label>
          ))}
        </div>

        {!isSubmitted ? (
          <button
            className={styles.submitButton}
            onClick={handleSubmit}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                handleSubmit();
              }
            }}
            disabled={!selectedOption}
            type="button"
            aria-label="Submit answer"
            tabIndex={0}
          >
            Check Answer
          </button>
        ) : (
          <div className={styles.resultContainer}>
            <div className={clsx(styles.resultMessage, { [styles.correctResult]: isCorrect, [styles.incorrectResult]: !isCorrect })}>
              {isCorrect ? '✓ Correct!' : '✗ Incorrect'}
            </div>
            <button
              className={styles.resetButton}
              onClick={handleReset}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault();
                  handleReset();
                }
              }}
              type="button"
              aria-label="Try again"
              tabIndex={0}
            >
              Try Again
            </button>
          </div>
        )}

        {showExplanation && explanation && (
          <div className={styles.explanation} role="complementary">
            <h5 className={styles.explanationTitle}>Explanation:</h5>
            <p className={styles.explanationText}>{explanation}</p>
          </div>
        )}
      </div>
    </div>
  );
};

const MemoizedKnowledgeCheck = React.memo(KnowledgeCheck);
export default MemoizedKnowledgeCheck;