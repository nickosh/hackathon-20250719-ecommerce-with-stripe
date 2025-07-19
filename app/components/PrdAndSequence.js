import React from 'react';
import { encode } from 'plantuml-encoder';
import styles from '../styles/prd.module.css';
import { FiCheckCircle, FiArrowRight, FiCode, FiShoppingCart, FiGlobe, FiRefreshCw } from 'react-icons/fi';

const PrdAndSequence = ({ onProceed }) => {
  const plantUmlCode = `
  @startuml
  skinparam monochrome true
  skinparam shadowing false
  skinparam defaultFontName Arial
  skinparam sequence {
    ArrowColor #4a5568
    ActorBorderColor #4a5568
    LifeLineBorderColor #4a5568
    LifeLineBackgroundColor #f7fafc
    ParticipantBorderColor #4a5568
    ParticipantBackgroundColor #f7fafc
  }
  
  actor User as "User"
  participant "Web App" as App
  participant "Shopping Cart" as Cart
  participant "Stripe API" as Stripe

  User -> App: Add product to cart
  App -> Cart: Update cart state
  User -> App: Proceed to checkout
  App -> Stripe: Initiate payment session
  Stripe -> User: Show payment form
  User -> Stripe: Submit payment
  Stripe -> App: Payment success callback
  App -> User: Show success page
  @enduml
  `;

  const plantUmlUrl = `https://www.plantuml.com/plantuml/svg/${encode(plantUmlCode)}`;

  const productRequirements = [
    {
      title: "Stripe Payment Integration",
      description: "Implement secure payment processing using Stripe API with JPY currency support and proper error handling.",
      icon: <FiCheckCircle className={styles.icon} />
    },
    {
      title: "Shopping Cart System",
      description: "Develop client-side cart management with add/remove functionality, quantity adjustment, and real-time total calculation.",
      icon: <FiShoppingCart className={styles.icon} />
    },
    {
      title: "Responsive Product UI",
      description: "Create mobile-first product listings with responsive design that works across all device sizes.",
      icon: <FiGlobe className={styles.icon} />
    },
    {
      title: "Payment Callbacks",
      description: "Implement success and cancellation pages with proper state management and user feedback.",
      icon: <FiArrowRight className={styles.icon} />
    },
    {
      title: "Geographic Restrictions",
      description: "Enforce Japan-only transactions with proper validation and user messaging.",
      icon: <FiGlobe className={styles.icon} />
    },
    {
      title: "State Persistence",
      description: "Maintain cart state across page refreshes using client-side storage solutions.",
      icon: <FiRefreshCw className={styles.icon} />
    }
  ];

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>QA Hackathon: E-commerce Checkout Flow</h1>
      
      <div className={styles.section}>
        <h2 className={styles.sectionTitle}>
          <FiCode className={styles.icon} />
          Product Requirements
        </h2>
        <div>
          {productRequirements.map((req, index) => (
            <div key={index} className={styles.requirementItem}>
              <div className={styles.requirementTitle}>
                {req.icon} {req.title}
              </div>
              <div className={styles.requirementDesc}>{req.description}</div>
            </div>
          ))}
        </div>
      </div>

      <div className={styles.section}>
        <h2 className={styles.sectionTitle}>
          <FiArrowRight className={styles.icon} />
          Checkout Sequence Diagram
        </h2>
        <div className={styles.diagramContainer}>
          <img 
            src={plantUmlUrl} 
            alt="Checkout Sequence Flow" 
            className={styles.diagramImage}
            onError={(e) => {
              e.target.onerror = null;
              e.target.src = 'https://via.placeholder.com/800x400?text=Diagram+Loading+Failed';
            }}
          />
        </div>
      </div>

      <div className={styles.buttonContainer}>
        <button
          onClick={onProceed}
          className={styles.button}
        >
          Let's start the QA Hackathon <FiArrowRight style={{ marginLeft: '0.5rem' }} />
        </button>
      </div>
    </div>
  );
};

export default PrdAndSequence;