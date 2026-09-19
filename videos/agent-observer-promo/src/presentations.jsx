import React from 'react';
import {VisualById} from './FilmVisual.jsx';

// 路由分发：按 plan.shots[].component 路由到 FilmVisual 子组件。
// 无 component 标记（如 brand-only 镜头）回退到占位卡。
export function FeatureVisual({shot}) {
  if (!shot || !shot.component) {
    return null;
  }
  return <VisualById shot={shot} />;
}