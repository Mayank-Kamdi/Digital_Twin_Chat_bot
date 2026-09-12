/**
 * Vercel Speed Insights - Standalone Initialization
 * Extracted and adapted from @vercel/speed-insights v1.3.1
 */
(function() {
  'use strict';

  // Initialize the Speed Insights queue
  function initQueue() {
    if (window.si) return;
    window.si = function() {
      (window.siq = window.siq || []).push(arguments);
    };
  }

  // Check if running in browser environment
  function isBrowser() {
    return typeof window !== "undefined";
  }

  // Detect environment (development or production)
  function detectEnvironment() {
    try {
      const env = process.env.NODE_ENV;
      if (env === "development" || env === "test") {
        return "development";
      }
    } catch (e) {
      // process not defined, assume production
    }
    return "production";
  }

  function isDevelopment() {
    return detectEnvironment() === "development";
  }

  // Get the appropriate script source based on configuration
  function getScriptSrc(props) {
    if (props.scriptSrc) {
      return props.scriptSrc;
    }
    if (isDevelopment()) {
      return "https://va.vercel-scripts.com/v1/speed-insights/script.debug.js";
    }
    if (props.dsn) {
      return "https://va.vercel-scripts.com/v1/speed-insights/script.js";
    }
    if (props.basePath) {
      return props.basePath + "/speed-insights/script.js";
    }
    return "/_vercel/speed-insights/script.js";
  }

  // Main function to inject Speed Insights
  function injectSpeedInsights(props) {
    props = props || {};
    
    if (!isBrowser() || props.route === null) return null;
    
    initQueue();
    
    const src = getScriptSrc(props);
    
    // Check if script already loaded
    if (document.head.querySelector('script[src*="' + src + '"]')) return null;
    
    // Register beforeSend callback if provided
    if (props.beforeSend && window.si) {
      window.si('beforeSend', props.beforeSend);
    }
    
    // Create and configure the script element
    const script = document.createElement("script");
    script.src = src;
    script.defer = true;
    script.dataset.sdkn = "@vercel/speed-insights";
    script.dataset.sdkv = "1.3.1";
    
    if (props.sampleRate) {
      script.dataset.sampleRate = props.sampleRate.toString();
    }
    
    if (props.route) {
      script.dataset.route = props.route;
    }
    
    if (props.endpoint) {
      script.dataset.endpoint = props.endpoint;
    } else if (props.basePath) {
      script.dataset.endpoint = props.basePath + "/speed-insights/vitals";
    }
    
    if (props.dsn) {
      script.dataset.dsn = props.dsn;
    }
    
    if (isDevelopment() && props.debug === false) {
      script.dataset.debug = "false";
    }
    
    script.onerror = function() {
      console.log(
        "[Vercel Speed Insights] Failed to load script from " + src + 
        ". Please check if any content blockers are enabled and try again."
      );
    };
    
    document.head.appendChild(script);
    
    return {
      setRoute: function(route) {
        script.dataset.route = route || undefined;
      }
    };
  }

  // Initialize Speed Insights when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      injectSpeedInsights({
        debug: false,
        sampleRate: 1
      });
    });
  } else {
    // DOM already loaded
    injectSpeedInsights({
      debug: false,
      sampleRate: 1
    });
  }
})();
